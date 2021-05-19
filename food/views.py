from django.shortcuts import render,redirect
from .models import *
from django.shortcuts import render, get_object_or_404
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.base import TemplateView
from django.contrib.auth import login, authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

def item_list(request):
    return render(request, 'food/item_list.html', {})

def contact_us(request):
    return render(request, 'food/contact_list.html', {})    

def categories(request):
    categories=Category.objects.all()
    return render(request, 'food/categories.html', {'categories':categories})

def food_list(request,pk):
    category=get_object_or_404(Category, title=pk)
    items=Item.objects.filter(category=category.pk)
    return render(request, 'food/food_list.html', {'items':items,'category':category})

def single_list(request,pk):
    item=get_object_or_404(Item,pk=pk)
    return render(request, 'food/single_list.html', {'item':item})

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return render(request, 'food/item_list.html', {})
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm
	return render (request=request, template_name="food/register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return render(request, 'food/item_list.html', {})
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="food/login.html", context={"login_form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return render(request, 'food/item_list.html', {})

@login_required
def add_to_cart(request, pk):
    categories=Category.objects.all()
    item = get_object_or_404(Item, id=pk)
    user=request.user
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
    )
    order = Cart.objects.filter(user=request.user)
    c=1
    if order.exists():
        order = order[0]
        item.quantity = item.quantity-1
        item.save()
        if order.items.filter(item=item).exists():
            order_item.quantity += 1
            order_item.save()
            order.amount+=order_item.price()/order_item.quantity
            order.save()
            return render(request, 'food/my_cart.html', {'categories':categories,'c':c,'order':order})
        else:
            order.items.add(order_item)
            order.amount += order_item.price()
            order.save()
            return render(request, 'food/my_cart.html', {'categories':categories,'c':c,'order':order})
    else:
        order = Cart()
        order.user=user
        order.amount=order_item.price()
        order.save()
        order.items.add(order_item)
        order.save()
        item.quantity=item.quantity-1
        item.save()
        return render(request, 'food/my_cart.html', {'categories':categories,'c':c,'order':order})


def my_cart(request):
    categories=Category.objects.all()
    user=request.user
    order = Cart.objects.filter(user=request.user)
    c=0
    if order.exists():
        c=1
        order = order[0]
    return render(request, 'food/my_cart.html', {'categories':categories,'c':c,'order':order})   

@login_required
def remove_single_item_from_cart(request, pk):
    categories=Category.objects.all()
    user=request.user
    order = Cart.objects.filter(user=request.user)
    c=0
    if order.exists():
        c=1
        order = order[0]
    order_item = get_object_or_404(OrderItem,id=pk)
    item = get_object_or_404(Item,id=order_item.item.pk)
    item.quantity+=order_item.quantity
    item.save()
    order.amount=order_item.price()
    order_item.delete()
    order.save()
    if order.items.all().count()==0:
        order.delete()
        c=0
    return redirect("/my_cart", {'categories':categories,'c':c,'order':order})

def checkout(request):
    return render(request, 'food/checkout.html', {})

def thankyou(request):
    return render(request, 'food/thankyou.html', {})    
