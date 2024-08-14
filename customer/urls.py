"""
URL configuration for shopping project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from customer import views

urlpatterns = [
    path('layout', views.layout, name='layout'),
    path('index', views.index, name='index'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),

    #Register
    path('register', views.register, name='register'),
    path('check_username', views.check_username, name='check_username'),
    path('check_email', views.check_email, name='check_email'),
    path('check_contact', views.check_contact, name='check_contact'),
    path('store_register', views.store_register, name='store_register'),

    path('login', views.login, name='login'),
    path('login_check', views.login_check, name='login_check'),
    path('logout', views.logout, name='logout'),

    #Contact
    path('contact', views.contact, name='contact'),
    path('insert_contact', views.insert_contact, name='insert_contact'),

    #saler Registration
    path('saler_reg', views.saler_reg, name='saler_reg'),
    path('store_reg', views.store_reg, name='store_reg'),
    path('delete_reg/<int:id>', views.delete_reg, name='delete_reg'),
    path('edit_reg/<int:id>', views.edit_reg, name='edit_reg'),
    path('update_reg/<int:id>', views.update_reg, name='update_reg'),

    #Get Product
    path('product_list/<int:id>', views.product_list, name='product_list'),
    path('product_detail/<int:id>', views.product_detail, name='product_detail'),

    #Cart
    path('cart', views.cart, name='cart'),
    path('insert_cart', views.insert_cart, name='insert_cart'),
    path('delete_cart/<int:id>', views.delete_cart, name='delete_cart'),

    #CheckOut
    path('checkout', views.checkout, name='checkout'),
    path('store_checkout', views.store_checkout, name='store_checkout'),

    path('success', views.success, name='success'),
    path('payment', views.payment, name='payment'),
    
    #Order
    path('myorder', views.myorder, name='myorder'),

    #Invoice
    path('generate_invoice/<int:order_id>/', views.generate_invoice, name='generate_invoice'),
]
