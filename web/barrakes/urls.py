"""barrakes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from django.contrib.auth.views import LogoutView

from .apps.orders.views import OrderStatusView, OrderStatusRedirectView
from .apps.orders.views import create_new_order, change_order_status, order_list, order_status, change_product_status, order_items_list, product_listing, order_listing, homepage_view, create_order, receipt, print_receipt
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('dashboard/', homepage_view, name='homepage'),
    path('orders/', order_listing, name='order_list'),
    path('', RedirectView.as_view(url=reverse_lazy('order_add'), permanent=True)),
    path('orders/add/', create_order, name='order_add'),
    path('orders/<int:pk>/status/', OrderStatusRedirectView.as_view(), name='order_status_pk'),
    path('orders/<slug:slug>/status/', OrderStatusView.as_view(), name='order_status'),
    path('orders/<int:pk>/receipt/', receipt, name='order_receipt'),
    path('products/', product_listing, name='product_list'),
    path('ajax/orders/add/', create_new_order, name='ajax_new_order'),
    path('ajax/change_order_status/', change_order_status, name='change_order_status'),
    path('ajax/order_list', order_list, name='ajax_order_list'),
    path('ajax/orders/status/', order_status, name='ajax_order_status'),
    path('ajax/change_product_status/', change_product_status, name='change_product_status'),
    path('ajax/order_items/', order_items_list, name='ajax_order_items'),
    path('ajax/order/print', print_receipt, name='print_receipt')

]

admin.site.site_title = "Diablerraka admin"
admin.site.site_header = "Diablerraka admin"
