from django.urls import path
from . import views
from .forms import *
from django.contrib.auth import views as auth_views


app_name = 'store'

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),


    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),


    path('signup/', views.signup, name="signup"),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html', authentication_form=LoginForm), name='login'),

]