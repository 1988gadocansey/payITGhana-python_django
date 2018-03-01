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

class ClientUpdate(forms.ModelForm):
    # firstname = forms.CharField(max_length=254,required=True)
    # lastname = forms.CharField(max_length=254,required=True)
    #
    # phone = forms.IntegerField(required=True)
    # mobile_money_name = forms.CharField(max_length=254,required=True)
    # mobile_money_phone = forms.IntegerField(required=True)
    # referrer = forms.CharField(max_length=254,required=False)
    #
    # gender = forms.CharField(max_length=10)
    # address = forms.CharField(max_length=254,required=False)
    # email = forms.EmailField(required=False)

    class Meta:
        model = Client
        fields = ('user_id','firstname', 'lastname', 'gender', 'phone','address','mobile_money_name','mobile_money_phone','referrer','address')


