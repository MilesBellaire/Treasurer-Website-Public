from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(empty_value="Email")
    first_name = forms.CharField(empty_value="First Name", max_length=25)
    last_name = forms.CharField(empty_value="Last Name", max_length=25)


    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password1", "password2"]