from django.contrib import admin

# Register your models here.
from .models import Suppler, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug' , 'image','quantity',]
    class Meta:
        model = Product


admin.site.register(Suppler)
admin.site.register(Product, ProductAdmin)
