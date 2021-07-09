from django import forms
from django.apps import apps
from django.forms import  ModelForm
from .models import Suppler, Product
Item=apps.get_model('carts.Item')

class SupplerForm(ModelForm):
    class Meta:
        model = Suppler
        fields = '__all__'


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude=['slug']


class ItemForm(ModelForm):
    class Meta:
        model=Item
        fields=['quantity',]