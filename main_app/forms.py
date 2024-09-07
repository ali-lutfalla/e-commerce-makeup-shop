from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class UserSignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "input","placeholder":"username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "input","placeholder":"email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "input","placeholder":"password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "input","placeholder":"confirm password"}))
    class Meta:
        model = User
        fields = ('username', 'email')

class UserSignInForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserSignInForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder':'Username', 'class':'input'})
        self.fields['password'].widget.attrs.update({'placeholder':'Password', 'class':'input'})