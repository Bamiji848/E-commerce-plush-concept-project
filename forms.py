from django import forms
from .import models
from django.core import validators
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from plush_app.models import Login, Order
from plush_app.cart import Cart
from captcha.fields import CaptchaField
# from phonenumber_field.modelfields import PhoneNumberField



class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city','mobile_number','alternative_number']
        

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 26)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    


class ContactForm(forms.ModelForm):
    class Meta:
        model = models.Contact
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message'}),
        }


class Register(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required',widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Type Your Email Here'}))
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Username'}))
    captcha = CaptchaField()
    
        
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class EditProfileForm(UserChangeForm):

    class Meta():
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']


class LoginForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Password')

    class Meta:
        model = Login
        fields = ('email', 'password' )



