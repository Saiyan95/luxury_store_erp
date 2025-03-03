"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from apps.core.views import (
    dashboard, suppliers_list, sales_dashboard, 
    reports_dashboard, settings_dashboard, import_excel
)
from apps.inventory.views import (
    inventory_dashboard, product_list, category_list,
    add_product
)
from apps.finance.views import finance_dashboard, transaction_list
from apps.sales.views import add_sale, sales_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', lambda request: render(request, 'base.html', {})),
    path('', dashboard, name='dashboard'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('suppliers/', suppliers_list, name='suppliers_list'),
    path('sales/', sales_dashboard, name='sales_dashboard'),
    path('sales/add/', add_sale, name='add_sale'),
    path('sales/list/', sales_list, name='sales_list'),
    path('reports/', reports_dashboard, name='reports_dashboard'),
    path('inventory/', inventory_dashboard, name='inventory_dashboard'),
    path('inventory/products/', product_list, name='product_list'),
    path('inventory/products/add/', add_product, name='add_product'),
    path('inventory/categories/', category_list, name='category_list'),
    path('finance/', finance_dashboard, name='finance_dashboard'),
    path('finance/transactions/', transaction_list, name='transaction_list'),
    path('settings/', settings_dashboard, name='settings_dashboard'),
    path('import_excel/', import_excel, name='import_excel'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
