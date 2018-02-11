from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Client

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

        # model = Client
        # fields = ('firstname', 'lastname', 'gender', 'phone','address','mobile_money_name','mobile_money_phone','referrer')