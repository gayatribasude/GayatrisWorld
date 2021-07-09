from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.views.generic.list import ListView
from django.apps import apps
Product = apps.get_model('products', 'Product')


class SearchProductListView(ListView):
    template_name = 'search/productlistsearch.html'

    context_object_name = 'product' #object_list =product
    extra_context = {'title':'Search Result'}


    def get_queryset(self, *args, **kwargs):
        request=self.request
        query = request.GET.get('q')
        if query is not None:
            manyquery =Q(name__icontains=query) | Q(description__icontains=query)|Q(slug__icontains=query)
            return Product.objects.filter(manyquery).distinct()
        else:
            return Product.objects.none()

    def get_context_data(self,*args, **kwargs):
        context = super(SearchProductListView,self).get_context_data(*args,**kwargs)
        context['query'] = self.request.GET.get('q')
        return context