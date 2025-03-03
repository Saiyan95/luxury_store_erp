from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, F
from apps.inventory.models import Product, Category, Supplier, PurchaseOrder
from django.utils import timezone
from datetime import timedelta
from apps.sales.models import Sale
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

# Create your views here.

@login_required
def dashboard(request):
    # Get statistics
    total_products = Product.objects.count()
    total_sales = Sale.objects.count()
    total_suppliers = Supplier.objects.count()
    low_stock_products = Product.objects.filter(quantity__lt=F('reorder_point'))
    low_stock_count = low_stock_products.count()
    
    # Get recent sales
    recent_sales = Sale.objects.all().order_by('-sale_date')[:5]
    
    context = {
        'total_products': total_products,
        'total_sales': total_sales,
        'total_suppliers': total_suppliers,
        'low_stock_count': low_stock_count,
        'low_stock_products': low_stock_products[:5],
        'recent_sales': recent_sales,
    }
    return render(request, 'dashboard.html', context)

@login_required
def suppliers_list(request):
    suppliers = Supplier.objects.all()
    context = {
        'suppliers': suppliers,
        'active_suppliers': suppliers.filter(is_active=True).count(),
        'total_suppliers': suppliers.count(),
    }
    return render(request, 'suppliers/supplier_list.html', context)

@login_required
def sales_dashboard(request):
    context = {
        'total_sales': 0,  # We'll implement this when we create the sales models
        'recent_sales': [],
    }
    return render(request, 'sales/sales_dashboard.html', context)

@login_required
def reports_dashboard(request):
    context = {
        'total_inventory_value': Product.objects.aggregate(
            total_value=Sum(F('price') * F('quantity'))
        )['total_value'] or 0,
        'total_products': Product.objects.count(),
        'total_suppliers': Supplier.objects.count(),
        'recent_purchases': PurchaseOrder.objects.all()[:5],
    }
    return render(request, 'reports/reports_dashboard.html', context)

@login_required
def import_excel(request):
    print("Import Excel view accessed")  # Debugging line
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)

        # Read the Excel file
        df = pd.read_excel(uploaded_file_url)

        # Process the DataFrame and save to the database
        for index, row in df.iterrows():
            Product.objects.create(
                name=row['Name'],
                price=row['Price'],
                quantity=row['Quantity'],
                supplier=Supplier.objects.get(name=row['Supplier'])
            )

        messages.success(request, 'Excel file imported successfully!')
        return redirect('dashboard')
    return render(request, 'import_excel.html')

@user_passes_test(lambda u: u.is_superuser)
def settings_dashboard(request):
    context = {
        'total_users': User.objects.count(),
        'active_users': User.objects.filter(is_active=True).count(),
        'total_products': Product.objects.count(),
        'total_categories': Category.objects.count(),
        'total_suppliers': Supplier.objects.count(),
        'total_sales': Sale.objects.count(),
    }
    return render(request, 'settings/dashboard.html', context)
