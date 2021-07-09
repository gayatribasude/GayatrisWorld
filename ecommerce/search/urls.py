from django.urls import path

from . import views

urlpatterns =[
    path('',views.SearchProductListView.as_view(), name="searchproductlist"),
]