from django.apps import apps
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.http import is_safe_url

from .forms import AddressForm
BillingProfile=apps.get_model('orders','BillingProfile')
Address=apps.get_model('addresses','Address')
VisitorEmail=apps.get_model('accounts','VisitorEmail')



def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)
    user=request.user
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        print(request.POST)

        instance = form.save(commit=False)
        guest_visitor_id = request.session.get('guest_visitor_id')

        if user.is_authenticated:
            billingprofile, billingprofile_created = BillingProfile.objects.get_or_create(user=user, email=user.email)
            print(billingprofile)
        elif guest_visitor_id is not None:
            print("guest is", guest_visitor_id)
            visitor = VisitorEmail.objects.filter(email=guest_visitor_id)
            if visitor:
                visitor = visitor[0]
            billingprofile, billing_visitor_profile = BillingProfile.objects.get_or_create(email=visitor.email)
            print("billing profile for guest at address add",billingprofile)
        else:
            pass

        if billingprofile is not None:
            address_type = request.POST.get('address_type', 'shipping')
            instance.billing_profile = billingprofile
            print(instance)
            instance.address_type = address_type
            instance.save()
            request.session[address_type + "_address_id"] = instance.id
            print(address_type + "_address_id")
        else:
            print("Error here")
            return redirect("checkout_home")

        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
    return redirect("checkout_home")


def checkout_address_use_view(request):
    user=request.user
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if request.method=="POST":
        print("post data",request.POST)
        shipping_address=request.POST.get('shipping_address',None)
        print("shipping address from post",shipping_address)
        address_type=request.POST.get('address_type','shipping')
        guest_visitor_id = request.session.get('guest_visitor_id')
        print("addresstype",address_type)

        if user.is_authenticated:
            billingprofile, billingprofile_created = BillingProfile.objects.get_or_create(user=user, email=user.email)
            print(billingprofile)
        elif guest_visitor_id is not None:
            print("guest is", guest_visitor_id)
            visitor = VisitorEmail.objects.filter(email=guest_visitor_id)
            if visitor:
                visitor = visitor[0]
            billingprofile, billing_visitor_profile = BillingProfile.objects.get_or_create(email=visitor.email)
            print("billing profile for guest at address use", billingprofile)


        if shipping_address is not None:
            qs=Address.objects.filter(billing_profile=billingprofile,id=shipping_address)
            if qs.exists():
                request.session[address_type+"_address_id"]=shipping_address
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
        return redirect("checkout_home")



