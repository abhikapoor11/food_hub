from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('contact', views.contact_us, name='contact_us'),
    path('categories', views.categories, name='categories'),
    path('categories/<str:pk>', views.food_list, name='food_list'),
    path('item/<str:pk>', views.single_list, name='single_list'),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login_request"),
    path("logout", views.logout_request, name= "logout_request"),
    path("my_cart",views.my_cart,name="my_cart"),
    path('add-to-cart/<str:pk>/', views.add_to_cart, name='add_to_cart'),
    path('remove-single-item-from-cart/<str:pk>/', views.remove_single_item_from_cart,name='remove_single_item_from_cart'),
    path('checkout', views.checkout, name='checkout'),
    path('thankyou', views.thankyou, name='thankyou')
    
]