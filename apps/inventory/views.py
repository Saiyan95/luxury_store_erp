from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, F
from .models import Product, Category, Brand, Supplier, PurchaseOrder
from .forms import ProductForm

# Create your views here.

@login_required
def inventory_dashboard(request):
    # Get inventory statistics
    total_products = Product.objects.count()
    low_stock_products = Product.objects.filter(quantity__lt=10)
    total_value = Product.objects.aggregate(
        total=Sum(F('price') * F('quantity'))
    )['total'] or 0
    
    # Get category distribution
    categories = Category.objects.annotate(
        product_count=Count('products'),
        total_value=Sum(F('products__price') * F('products__quantity'))
    )
    
    context = {
        'total_products': total_products,
        'low_stock_products': low_stock_products,
        'total_value': total_value,
        'categories': categories,
    }
    return render(request, 'inventory/dashboard.html', context)

@login_required
def product_list(request):
    products = Product.objects.all().select_related('category', 'brand')
    context = {
        'products': products,
        'total_products': products.count(),
        'low_stock_count': products.filter(quantity__lte=5).count(),
    }
    return render(request, 'inventory/product_list.html', context)

@login_required
def category_list(request):
    categories = Category.objects.annotate(
        product_count=Count('products'),
        total_value=Sum(F('products__price') * F('products__quantity'))
    )
    context = {
        'categories': categories,
    }
    return render(request, 'inventory/category_list.html', context)

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" has been added successfully.')
            return redirect('product_list')
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'title': 'Add New Product',
    }
    return render(request, 'inventory/product_form.html', context)
