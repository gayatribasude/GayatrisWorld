from django import forms
from django.apps import apps
from .models import Item
Address=apps.get_model('addresses','Address')

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class VisitorForm(forms.Form):
    email = forms.EmailField()


class AddressForm(forms.ModelForm):
    class Meta:
        model=Address
        fields='__all__'
        exclude = ['billing_profile', 'address_type']

class ItemForm(forms.ModelForm):
    class Meta:
        model=Item
        fields=['quantity']