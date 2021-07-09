from django.contrib import admin
from .models import Order,BillingProfile
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','billing_profile','updated','finaltotal')


class BillingAdmin(admin.ModelAdmin):
    list_display = ('id','email')

admin.site.register(Order,OrderAdmin)
admin.site.register(BillingProfile,BillingAdmin)