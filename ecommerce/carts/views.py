from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from .forms import LoginForm, VisitorForm, AddressForm,ItemForm

from .models import Item,Cart

Cart  # ,Item
Product = apps.get_model('products','Product')
Order = apps.get_model('orders','Order')
BillingProfile = apps.get_model('orders','BillingProfile')
VisitorEmail=apps.get_model("accounts","VisitorEmail")
Address=apps.get_model('addresses','Address')
Invoice=apps.get_model('invoices','Invoice')



def cartshome(request):

    cart_id = request.session.get("cart_id",None)
    queryset =Cart.objects.filter(id=cart_id)
    if queryset.count()==1: # either it will be 0 or 1
        cart = queryset.first()


        if request.user.is_authenticated and cart.user is None:
            cart.user = request.user
            cart.save()

        print(cart)


    else:
        cart = Cart.objects.newcart(user=request.user)
        print(request.user)
        request.session['cart_id']=cart.id

    #product = cart.products.all()
    #total = 0
    #for x in product:
        #total =total + x.price
    #print(total)
    #cart.total =total
    #cart.save()

    return render(request, "carts/carts.html", {"cart": 'cart','title':'Cart'})


def cart_home(request):
    cart, _ =Cart.objects.new_or_get(request)
    print(cart.items.all())
    return render(request,"carts/carts.html",{"cart":cart,'title':'Cart'})

def updatecart(request):
    productid =request.POST.get("productid")
    print(productid)
    item_quantity=request.POST.get("quantity")
    print(item_quantity)

    product = Product.objects.get(id=productid)
    print(product)

    cart, _ = Cart.objects.new_or_get(request)
    print(cart)

    item_object, created = Item.objects.get_or_create(product=product, cart_in_item=cart)
    if item_quantity is not None:
        if int(item_quantity)>=1:
            item_object.quantity=int(item_quantity)
            item_object.save()
    else:
        pass
    if item_object in cart.items.all():

        item_object.quantity=0
        item_object.save()
        cart.items.remove(item_object)
        print("removed")
        added = False
    else:

        cart.items.add(item_object)
        print("added")
        added = True
    cart.save()
    request.session['cart_items'] = cart.items.count()


    if request.is_ajax():
        json_data={
            "added":added,
            "removed": not added,
            "cartCount":cart.items.count()
        }
        return JsonResponse(json_data)

    return redirect("cartshome")
    #return render(request, "products/productdetails.html", {'item_object': item_object})

def checkout_home(request):
    current_site = get_current_site(request)
    cart, cart_created = Cart.objects.new_or_get(request)
    messages=""
    order=None
    if cart_created or cart.items.count()==0:
        return redirect("cartshome")

    user=request.user
    billingprofile=None
    login_form = LoginForm()
    visitor_form=VisitorForm()
    address_form=AddressForm()
    billing_address_form=AddressForm()
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)

    guest_visitor_id=request.session.get('guest_visitor_id')

    if user.is_authenticated:
        billingprofile ,billingprofile_created =BillingProfile.objects.get_or_create(user=user,email=user.email)
        print(billingprofile)
    elif guest_visitor_id is not None:
        print("guest is",guest_visitor_id)
        visitor=VisitorEmail.objects.filter(email=guest_visitor_id)
        if visitor:
            visitor=visitor[0]
        billingprofile ,billing_visitor_profile=BillingProfile.objects.get_or_create(email=visitor.email)
    else:
        pass
    address_list=None
    if billingprofile is not None:
        address_list=Address.objects.filter(billing_profile=billingprofile)
        print("address_list",address_list)
        order_qs=Order.objects.filter(billing_profile=billingprofile,cart=cart,active=True)
        if order_qs.count()==1:
            order=order_qs.first()
        else:
            old_order_qs=Order.objects.exclude(billing_profile=billingprofile).filter(cart=cart,active=True)
            if old_order_qs.exists():
                old_order_qs.update(active=False)
            order=Order.objects.create(billing_profile=billingprofile,cart=cart,confirm=False)

        if shipping_address_id:
            order.shipping_address=Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id:
            order.billing_address=Address.objects.get(id=billing_address_id)
            del request.session['billing_address_id']
        if billing_address_id or shipping_address_id:
            order.save()

# yaahaa hunn 1 mark done huaa yaahaa
        if request.method=="POST":
            if guest_visitor_id:

                # yaha main jaana chahiye
                send_mail(
                "Confirm Order",
                    'Confirm your order \n- %s/%s/%s click on this link...' % (
                        current_site.name,"carts/confirm_order",order.id
                    )
                    ,
                settings.EMAIL_HOST_USER,
                [guest_visitor_id],
                fail_silently=True,
                )



                messages="We have sent email ! Confirm your order from link in mail."
                print("order_id",order.id)
                print(current_site.name)
                print(current_site.domain)

            if request.user.is_authenticated:
                order.confirm=True
                order.save()


        is_done=order.check_done()

        if is_done:
            order.mark_done()

            Invoice.objects.create(order_invoice=order)
            print("invoice",Invoice)
            print("last moment cart_id",request.session["cart_id"])


            del request.session["cart_id"]
            request.session['cart_items']=0

            # create session for invoice
            request.session['order_invoice']=order.id
            print(request.session.get("order_invoice"))

            return redirect("checkout_success")

    return render(request,"carts/checkout.html",{"object":order,"billingprofile":billingprofile,"form":login_form,"visitor_form":visitor_form,"address_form":address_form,"billing_address_form":billing_address_form,"address_list":address_list,"messages":messages,'title':'Checkout'})



def checkout_success(request):

    guest_visitor_id = request.session.get('guest_visitor_id')
    print(guest_visitor_id)
    get_visitor=VisitorEmail.objects.filter(email=guest_visitor_id)
    print(get_visitor)
    VisitorEmail.objects.all().update(active=False)
    order_invoice_session=request.session.get('order_invoice')


    if request.method=="POST":

        return redirect("invoice",id=order_invoice_session)

    return render(request,'checkout_success.html',{'title':'Successful Checkout'})



def confirm_order(request,order_id):

    if request.method=="POST":
        order=Order.objects.get(id=order_id)
        order.confirm=True
        order.save()


        return redirect("checkout_home")
    return render(request,"carts/confirm_order.html",{'title':'Confirm Your Order'})

