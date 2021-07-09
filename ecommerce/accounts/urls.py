
from django.urls import path

from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('contact/',views.conatct_page,name='contact'),
    path('login/',views.login_view,name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login1/', views.LoginView.as_view(), name='loginview'),
    path('visitor/',views.visitor_view,name='visitor_view'),
    path('login/account',views.account_view,name='account'),
    path('receivedcontacts/',views.ContactList.as_view(),name='receivedcontacts')


]
