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
from saler import views

urlpatterns = [
    path('layout', views.layout, name='layout'),
    path('dashboard', views.dashboard, name='dashboard'),

    path('login', views.login, name='login'),
    path('login_check', views.login_check, name='login_check'),
    path('logout', views.logout, name='logout'),

    #Product
    path('add_product', views.add_product, name='add_product'),
    path('store_product', views.store_product, name='store_product'),
    path('all_product', views.all_product, name='all_product'),
    path('delete_product/<int:id>', views.delete_product, name='delete_product'),
    path('edit_product/<int:id>', views.edit_product, name='edit_product'),
    path('update_product/<int:id>', views.update_product, name='update_product'),

    #Order
    path('order', views.order, name='order'),
    path('order_detail/<int:id>', views.order_detail, name='order_detail'),
    path('search_order', views.search_order, name='search_order'),
    path('gen_excel_order/', views.gen_excel_order, name='gen_excel_order'),
    path('gen_pdf_orders/', views.gen_pdf_orders, name='gen_pdf_orders'),
]
