from django.core.validators import MinLengthValidator
from django.db import models

# Create your models here.
ADDRESS_TYPES=(('billing','Billing'),
               ('shipping','Shipping'),)

class Address(models.Model):
    billing_profile=models.ForeignKey('orders.BillingProfile',on_delete=models.CASCADE)
    full_name =models.CharField(max_length=25,blank=False,null=False)
    address_type=models.CharField(max_length=20,choices=ADDRESS_TYPES)
    #address_line_1 =models.CharField(max_length=20)
    #address_line_2=models.CharField(max_length=20)

    #city=models.CharField(max_length=20)
    #country=models.CharField(max_length=20)
    #state=models.CharField(max_length=20)
    address_line=models.TextField(verbose_name="Address",blank=False,null=False)
    postal_code=models.PositiveSmallIntegerField(blank=False,null=False,)
    contact_no = models.PositiveIntegerField(blank=False,null=False,)


    def get_address(self):
        return "{name}  ,{line1}\n :{postal}\n ,{contact}".format(
            name=self.full_name,
            line1=self.address_line,

            postal=self.postal_code,
            contact=self.contact_no,
        )

    def __str__(self):
        return str(self.address_line)

