from django.urls import path
from . import views
urlpatterns=[
    path('add_address',views.checkout_address_create_view,name='add_address'),
    path('use_address',views.checkout_address_use_view, name='use_address'),
]