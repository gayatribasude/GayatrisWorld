from django.db import models


# Create your models here.
from django.db.models.signals import post_save


class Invoice(models.Model):
    order_invoice=models.OneToOneField('orders.Order',on_delete=models.CASCADE)
    invoice_pdf=models.FileField(upload_to="static_cdn/media_root")

def post_save_invoice(sender,instance,**kwargs):
    invoice=Invoice.objects.filter(id=instance.id)
    invoice.objects.update(invoice_pdf="http://127.0.0.1:8000/invoice/download="+{{id}})

"""
def post_save_invoice_for_product_count_update(sender,instace,created,**kwargs):
    invoice=Invoice.object.get(id=instace.id)
    cart_item=invoice.order_invoice.cart.items.all()
    for i in cart_item:
        print(i)


post_save.connect(post_save_invoice_for_product_count_update,sender=Invoice)
"""