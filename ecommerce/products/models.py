from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.core.validators import MinLengthValidator

from .utils import get_client_ip
from django.db import models

# Create your models here.
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver, Signal

from django.urls import reverse

from .utils import unique_slug_generator
User=settings.AUTH_USER_MODEL

class Suppler(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(null=False,blank=False)
    phoneno = models.BigIntegerField(null=False,blank=False)
    gstno = models.CharField(max_length=13,validators=[MinLengthValidator(13)])
    address = models.TextField(null=True,blank=False)

    def __str__(self):
        return self.name


class ProductManager(models.Manager):
    # using this function in classview by get_object()
    def get_by_slug(self,slug):
        return self.get_queryset().filter(slug=slug)
    #here self.get_queryset() == Product.objects


class Product(models.Model):
    name = models.CharField(max_length=30,blank=False,null=False)
    slug = models.SlugField(blank=True,unique=True)
    description=models.TextField(null=True,blank=True)
    price = models.DecimalField(decimal_places=2,max_digits=20,null=False,blank=False)
    image = models.ImageField(null=True,blank=False, upload_to='static_cdn/media_root')
    quantity = models.PositiveIntegerField(null=True,blank=False)
    date = models.DateTimeField(auto_now_add=True)
    supplername =models.ForeignKey(Suppler,on_delete=models.CASCADE)

    objects = ProductManager()
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("productdetails",kwargs={"slug:self.slug"})

    def double_price(self):
        return str(self.price*2)


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)

def product_quauntity_at_2(sender,instance,*args,**kwargs):
    product=Product.objects.get(id=instance.id)
    quantity=product.quantity
    name=product.name
    slug=product.slug
    if quantity == 2 or quantity < 2:
        print("Email is getting send to notifying quantity")
        message="Product name:"+ name+"\nQuantity:"+ str(quantity)+"\nProductslug:"+slug
        emailfrom = settings.EMAIL_HOST_USER
        emaillto = settings.EMAIL_HOST_USER
        send_mail('Quantity Low',
                  message,
                  emailfrom,
                  [emaillto],
                  fail_silently=False,
                  )
post_save.connect(product_quauntity_at_2,sender=Product)