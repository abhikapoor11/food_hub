from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    address = forms.CharField(required=False)
    gender = forms.CharField(required=True)

    class Meta:
	    model = User
	    fields = ("first_name","last_name", "username","gender","email", "password1", "password2","address")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user = authenticate(request, username=username, password=password)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.address = self.cleaned_data['address']
        user.gender = self.cleaned_data['gender']		
        if commit:
            user.save()
        return user