from django.urls import path
from . import views
urlpatterns=[
    path('sales',views.SalesView.as_view(),name='analysis'),
    path('sales/ajax',views.SalesAjaxView.as_view(),name='analysis_ajax'),
    path('orderlist',views.OrderList.as_view(),name='orderlist'),
    path('orderlist/orderdetails/<int:pk>',views.OrderDetails.as_view(),name='orderdetails'),
    path('orders/orderupdate/<int:pk>',views.UpdateOrder.as_view(),name='updateorder'),
]