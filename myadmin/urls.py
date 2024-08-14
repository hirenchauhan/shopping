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
from myadmin import views

urlpatterns = [
    path('layout', views.layout, name='layout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('common_form', views.common_form, name='common_form'),
    path('common_table', views.common_table, name='common_table'),

    #Login
    path('login', views.login, name='login'),
    path('login_check', views.login_check, name='login_check'),
    path('logout', views.logout, name='logout'),

    #State
    path('add_state', views.add_state, name='add_state'),
    path('all_state', views.all_state, name='all_state'),
    path('insert_state', views.insert_state, name='insert_state'),
    path('del_state/<int:id>', views.del_state, name='del_state'),
    path('edit_state/<int:id>', views.edit_state, name='edit_state'),
    path('update_state/<int:id>', views.update_state, name='update_state'),

    #City
    path('add_city', views.add_city, name='add_city'),
    path('all_city', views.all_city, name='all_city'),
    path('insert_city', views.insert_city, name='insert_city'),
    path('del_city/<int:id>', views.del_city, name='del_city'),
    path('edit_city/<int:id>', views.edit_city, name='edit_city'),
    path('update_city/<int:id>', views.update_city, name='update_city'),

    #Area
    path('add_area', views.add_area, name='add_area'),
    path('insert_area', views.insert_area, name='insert_area'),
    path('all_area', views.all_area, name='all_area'),
    path('del_area/<int:id>', views.del_area, name='del_area'),
    path('edit_area/<int:id>', views.edit_area, name='edit_area'),
    path('update_area/<int:id>', views.update_area, name='update_area'),

    #Customer
    path('customer', views.customer, name='customer'),
    path('view_customer/<int:id>', views.view_customer, name='view_customer'),
    path('verify/<int:id>', views.verify, name='verify'),
    path('search_customer', views.search_customer, name='search_customer'),
    path('gen_excel_customer/', views.gen_excel_customer, name='gen_excel_customer'),
    path('gen_pdf_customer/', views.gen_pdf_customer, name='gen_pdf_customer'),

    #Contact
    path('all_inquery', views.all_inquery, name='all_inquery'),
    path('del_inquery/<int:id>', views.del_inquery, name='del_inquery'),

    #Catagories
    path('add_categories', views.add_categories, name='add_categories'),
    path('store_categories', views.store_categories, name='store_categories'),
    path('all_categories', views.all_categories, name='all_categories'),
    path('delete_cat/<int:id>', views.delete_cat, name='delete_cat'),
    path('edit_cat/<int:id>', views.edit_cat, name='edit_cat'),
    path('update_cat/<int:id>', views.update_cat, name='update_cat'),

    #SubCatagories
    path('add_subcategories', views.add_subcategories, name='add_subcategories'),
    path('store_subcat', views.store_subcat, name='store_subcat'),
    path('all_subcategories', views.all_subcategories, name='all_subcategories'),
    path('delete_subcat/<int:id>', views.delete_subcat, name='delete_subcat'),
    path('edit_subcat/<int:id>', views.edit_subcat, name='edit_subcat'),
    path('update_subcat/<int:id>', views.update_subcat, name='update_subcat'),

    #Saler
    path('saler', views.saler, name='saler'),
    path('detail_salers/<int:id>', views.detail_salers, name='detail_salers'),
    path('saler_verify/<int:id>', views.saler_verify, name='saler_verify'),
    path('search_saler', views.search_saler, name='search_saler'),
    path('gen_excel_saler/', views.gen_excel_saler, name='gen_excel_saler'),
    path('gen_pdf_saler/', views.gen_pdf_saler, name='gen_pdf_saler'),

    #Order
    path('order', views.order, name='order'),
    path('order_detail/<int:id>', views.order_detail, name='order_detail'),
    path('search_orders', views.search_orders, name='search_orders'),
    path('gen_excel_order/', views.gen_excel_order, name='gen_excel_order'),
    path('gen_pdf_orders/', views.gen_pdf_orders, name='gen_pdf_orders'),
]
