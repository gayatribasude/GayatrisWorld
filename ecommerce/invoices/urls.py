from django.urls import path
from . import views

urlpatterns=[
    #path('download=<id:id>',views.GeneratePdf.as_view(),name="invoice"),
    path('download=<int:id>',views.generatepdf_view,name="invoice"),
]