

from django.urls import path
from . import views


urlpatterns = [
    path('',views.cart_home, name="cartshome"),
    path('updatecart/',views.updatecart, name = "updatecart"),
    path('checkout_home/',views.checkout_home,name="checkout_home"),
    path('checkout_success',views.checkout_success,name="checkout_success"),

    path('confirm_order/<int:order_id>/',views.confirm_order,name="confirm_order"),
]
