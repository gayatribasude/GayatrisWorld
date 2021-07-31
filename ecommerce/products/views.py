from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, FormMixin

from django.views.generic.list import ListView


from .forms import SupplerForm, ProductForm, ItemForm
from .models import Product
Cart = apps.get_model('carts','Cart')
Order=apps.get_model('orders','Order')




class ProductListView(ListView):
    # login_url = '/login/'
    # redirect_field_name = 'productlist'
    template_name = 'products/productlist.html'
    queryset = Product.objects.all() #it returns object_list
    context_object_name = 'product' #object_list =product
    extra_context = {'title':'Product'}
    paginate_by = 6
    #ordering = ['-date']


class ProductDetailSlugView(FormMixin,DetailView):
    form_class = ItemForm
    template_name = 'products/productdetails.html'
    queryset = Product.objects.all() #it returns object
    context_object_name = 'product' # object==product

    extra_context = {'title':'Product Details'}
    def get_context_data(self, *args, **kwargs):
        request = self.request
        context = super(ProductDetailSlugView,self).get_context_data(**kwargs)
        cart ,_ = Cart.objects.new_or_get(request)
        context['cart']=cart
        return context
""""
    def get_object(self, *args,**kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        product = Product.objects.get_by_slug(slug)
        if product is None:
            raise Http404("Product does not exists")
        return product



    


# @receiver(pre_save, sender=Product)
#def pre_save_product(sender, instance, *args, **kwargs):
#    if not instance.slug:
#        instance.slug = unique_slug_generator(instance)


#pre_save.connect(pre_save_product(instance=), sender=Product)"""



class CreateSuppler(LoginRequiredMixin,TemplateView):
    form = SupplerForm
    template_name = "products/createsuppler.html"
    extra_context = {'title': 'Create Suppler'}

    def get(self, request, *args, **kwargs):
        form=self.form()
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form=self.form(request.POST)

        if form.is_valid():
            print(form.cleaned_data['quantity'])
            form.save()

            return HttpResponseRedirect('/')
        return render(request,self.template_name,{'form':form})





class CreateProduct(LoginRequiredMixin,CreateView):
    form = ProductForm
    template_name = "products/createproduct.html"
    extra_context = {'title': 'Create Product'}

    def get(self, request, *args, **kwargs):
        form=self.form()
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form=self.form(request.POST,request.FILES)
        if form.is_valid():
            print(form.cleaned_data)

            form.save()

            return redirect("productlist")

        return render(request,self.template_name,{'form':form})

class UpdateProduct(LoginRequiredMixin,UpdateView):
    model = Product
    success_url = '/product/'
    fields = ['name','description','price','image','quantity','supplername']
    template_name = 'products/updateproduct.html'
    extra_context = {'title': 'Update Product'}




def product_purchase_analysis(request):
    order=Order.objects.filter(confirm=True)
    d = {}
    list_product=[]
    list_quantity=[]
    for o in order:
        cart=o.cart
        items=cart.items.all()
        for i in items:
            print(i)
            product=i.product.slug
            print(product)
            quantity = i.quantity
            print(quantity)
            if d.get(product) is not None:
                d[product]+=quantity
            else:
                d[product]=quantity

    for i in d:
        list_product.append(i)
    for i in d.values():
        list_quantity.append(i)
    data={
        "product":list_product,"quantity":list_quantity,
    }

    return JsonResponse(data)

class ProductPurchase(View):
    def get(self,request,*args,**kwargs):
        return render(request,'products/productanalysis.html',{'title':'Trends'})