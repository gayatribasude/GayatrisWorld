import datetime
import math
import django
from django.apps import apps
from django.conf import settings
from django.db import models
from django.db.models import Avg, Sum, Count
from django.db.models.signals import post_save, pre_save
from django.utils import timezone

Cart=apps.get_model('carts','Cart',require_ready=False)
#Product=apps.get_model('products.Product')
User=settings.AUTH_USER_MODEL



STATUS =(
    ('created','Created'),
    ('paid','Paid'),
    ('shipped','Shipped'),
    ('refunded','Refunded')
)


class OrderManagerQuerySet(models.query.QuerySet):
    def recent(self):
        return self.order_by("-updated", "-timestamp")

    def get_sales_breakdown(self):
        recent = self.recent().not_refunded()
        recent_data = recent.totals_data()
        recent_cart_data = recent.cart_data()
        shipped = recent.not_refunded().by_status(status='created')
        shipped_data = shipped.totals_data()
        paid = recent.by_status(status='paid')
        paid_data = paid.totals_data()
        data = {
            'recent': recent,
            'recent_data': recent_data,
            'recent_cart_data': recent_cart_data,
            'shipped': shipped,
            'shipped_data': shipped_data,
            'paid': paid,
            'paid_data': paid_data
        }
        return data

    def by_weeks_range(self, weeks_ago=0, number_of_weeks=1):
        if number_of_weeks > weeks_ago:
            number_of_weeks = weeks_ago
        days_ago_start = weeks_ago * 7  # days_ago_start = 49
        days_ago_end = days_ago_start - (number_of_weeks * 7)  # days_ago_end = 49 - 14 = 35
        start_date = timezone.now() - datetime.timedelta(days=days_ago_start)
        end_date = timezone.now() - datetime.timedelta(days=days_ago_end)
        return self.by_range(start_date, end_date=end_date)

    def by_range(self, start_date, end_date=None):
        if end_date is None:
            return self.filter(updated__gte=start_date)
        return self.filter(updated__gte=start_date).filter(updated__lte=end_date)

    def by_date(self):
        now = timezone.now() - datetime.timedelta(days=1)
        return self.filter(updated__day__gte=now.day)

    def totals_data(self):
        return self.aggregate(Sum("finaltotal"), Avg("finaltotal"))

    def cart_data(self):
        return self.aggregate(
            Sum("cart__items__item_total"),
            #Sum("finaltotal"),
            Avg("cart__items__item_total"),
            #Avg("finaltotal"),
            Count("cart__items")
            #Count("finaltotal"),
        )

    def by_status(self, status="shipped"):
        return self.filter(status=status)

    def not_refunded(self):
        return self.exclude(status='refunded')

    def by_request(self, request):
        user=request.user
        guest_visitor_id = request.session.get('guest_visitor_id')

        if user.is_authenticated:
            billingprofile, billingprofile_created = BillingProfile.objects.get_or_create(user=user, email=user.email)
            print(billingprofile)
        elif guest_visitor_id is not None:
            print("guest is", guest_visitor_id)
            visitor = apps.get_model("accounts","VisitorEmail").objects.filter(email=guest_visitor_id)
            if visitor:
                visitor = visitor[0]
            billingprofile, billing_visitor_profile = BillingProfile.objects.get_or_create(email=visitor.email)
        return self.filter(billing_profile=billingprofile)

    def not_created(self):
        return self.exclude(status='created')


class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderManagerQuerySet(self.model, using=self._db)

class Order(models.Model):
    billing_profile =models.ForeignKey('orders.BillingProfile',on_delete=models.CASCADE,null=True,blank=True)
    ordered =models.CharField(default='True', max_length=10)
    shipping_address=models.ForeignKey('addresses.Address',related_name="shipping",on_delete=models.CASCADE,blank=True,null=True)
    billing_address=models.ForeignKey('addresses.Address',related_name="billing",on_delete=models.CASCADE,blank=True,null=True)
    status = models.CharField(choices=STATUS,default='created',max_length=20)
    shipping_total =models.DecimalField(max_digits=100, default=20,decimal_places=2)
    finaltotal = models.DecimalField(default=0.00, max_digits=30, decimal_places=2)
    cart = models.ForeignKey('carts.Cart',on_delete=models.CASCADE)
    active =models.BooleanField(default=True)
    updated=models.DateTimeField(auto_now=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    confirm=models.BooleanField()

    objects=OrderManager()

    def __str__(self):
        return str(self.id)

    def get_items(self):
        items=self.cart.items.all()
        return items

    #check whether all the required fields got its value or not
    def check_done(self):
        billing_profile=self.billing_profile
        shipping_address=self.shipping_address
        billing_address=self.billing_address
        finaltotal=self.finaltotal
        confirm=self.confirm

        if billing_profile and billing_address and shipping_address and finaltotal and confirm >0:
            return True
        else:
            return False

    #update product count in Product table only if order is confirm
    def mark_done(self):
        if self.check_done():
            items=self.cart.items.all()
            for i in items:
                product=i.product
                quantity=i.quantity
                print("product",product)
                print("quantity",quantity)
                project_object=apps.get_model('products.Product').objects.get(id=product.id)
                project_object.quantity=project_object.quantity-quantity
                project_object.save()

            self.status='created'
            self.save()
        return self.status

    #update order total with additional costs
    def update_total(self):
        cart_total = self.cart.finaltotal
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total, shipping_total])
        formatted_total = format(new_total, '.2f')
        print("formatted_total",formatted_total)
        self.finaltotal = formatted_total
        self.save()
        return new_total


def post_save_order_finaltotal(sender,instance,created,*args,**kwargs):
    if not created:
        order = instance
        time = timezone.now()
        cart_finaltotal = order.cart.finaltotal
        order_shipping = order.shipping_total
        print("cart_finaltotal", cart_finaltotal)
        print("order_shipping", order_shipping)
        order.updated = time
        print("time", time)
        new_total = cart_finaltotal + order_shipping
        order.finaltotal = new_total
        print("order_finaltotal", new_total)

    if created:
        instance.update_total()


post_save.connect(post_save_order_finaltotal,sender=Order)

def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.finaltotal
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()

post_save.connect(post_save_cart_total, sender=Cart)

#After creating order, update the total (shipping+card_total)
def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        print("Updating... first")
        instance.update_total()

post_save.connect(post_save_order, sender=Order)

#It is nothing but the profile of user who places order (whether it is admin,employee or customer)
class BillingProfile(models.Model):
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    email=models.EmailField()
    active=models.BooleanField(default=True)
    update=models.DateTimeField(auto_now=True)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


def user_created_receiver(sender,instance,created,*args,**kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance)

#whenever theres a new admin or employee at that time billing profile gets created
post_save.connect(user_created_receiver,sender=User)