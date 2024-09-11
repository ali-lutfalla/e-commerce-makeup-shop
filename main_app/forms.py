from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Product, Category

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

class ProductFilterForm(forms.Form):
    title = forms.CharField(required=False, label='Title', widget=forms.TextInput(attrs={"class": "input","placeholder":"Name of the product"}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label='Category', widget=forms.CheckboxSelectMultiple())
    price_min = forms.DecimalField(required=False, label='Min Price', decimal_places=2, max_digits=10, widget=forms.NumberInput(attrs={"class": "input"}))
    price_max = forms.DecimalField(required=False, label='Max Price', decimal_places=2, max_digits=10, widget=forms.NumberInput(attrs={"class": "input"}))
    brands = forms.MultipleChoiceField(
        choices=[(brand, brand) for brand, _ in Product.BRANDS],
        required=False,
        label='Brands',
        widget=forms.CheckboxSelectMultiple()
    )
    