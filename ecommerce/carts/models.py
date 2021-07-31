import datetime

from django.apps import apps
from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, m2m_changed, post_save
from django.dispatch import receiver
from decimal import Decimal


class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
            
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
            
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,blank=True, on_delete=models.CASCADE)
    items=models.ManyToManyField('carts.Item',blank=True)
    total = models.DecimalField(default=0.00, max_digits=30, decimal_places=2)
    finaltotal = models.DecimalField(default=0.00, max_digits=30,decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = CartManager()

    def __str__(self):
        return str(self.id)

class Item(models.Model):
    cart_in_item=models.ForeignKey('Cart',on_delete=models.CASCADE,null=True,blank=True)
    product=models.ForeignKey('products.Product',null=True,blank=True,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    item_total=models.DecimalField(decimal_places=2,default=0.00,max_digits=30)

    def __str__(self):
        return str(self.id)

def item_total_receiver(sender,instance,*args,**kwargs):
    instance.item_total=instance.product.price * instance.quantity

pre_save.connect(item_total_receiver,sender=Item)


def total_cart_receiver(sender, instance, action,*args, **kwargs):
    item=instance.items.all()
    print(item)
    total=0
    for i in item:
        total=total+(i.item_total)
    print(total)
    instance.total=total
    instance.save()


m2m_changed.connect(total_cart_receiver, sender=Cart.items.through)



def finaltotal_receiver(sender, instance, *args, ** kwargs):
    if instance.total ==0:
        instance.finaltotal = instance.total
    else:
        instance.finaltotal = instance.total +00


pre_save.connect(finaltotal_receiver, sender=Cart)
