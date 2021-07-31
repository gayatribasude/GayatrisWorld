
from django.urls import path
from .views import ProductListView, ProductDetailSlugView, CreateSuppler, CreateProduct, UpdateProduct,product_purchase_analysis,ProductPurchase

urlpatterns = [
    path('',ProductListView.as_view(), name = 'productlist'),
    path('createsuppler',CreateSuppler.as_view(),name = 'createsuppler'),
    path('createproduct',CreateProduct.as_view(),name = 'createproduct'),
    path('updateproduct/<slug:slug>',UpdateProduct.as_view(),name = 'updateproduct'),
    path('details/<slug:slug>',ProductDetailSlugView.as_view(), name='productdetails'),
    path('analysis/purchase',product_purchase_analysis,name='productanalysis'),
    path('analysis/purchase/view',ProductPurchase.as_view(),name='analysis_view')
]


