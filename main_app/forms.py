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
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username

class UserSignInForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserSignInForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder':'Username', 'class':'input'})
        self.fields['password'].widget.attrs.update({'placeholder':'Password', 'class':'input'})