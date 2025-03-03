from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, F
from apps.inventory.models import Product, PurchaseOrder

# Create your views here.

@login_required
def finance_dashboard(request):
    # Calculate financial statistics
    total_inventory_value = Product.objects.aggregate(
        total=Sum(F('price') * F('quantity'))
    )['total'] or 0
    
    total_purchase_orders = PurchaseOrder.objects.aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    context = {
        'total_inventory_value': total_inventory_value,
        'total_purchase_orders': total_purchase_orders,
        'recent_transactions': PurchaseOrder.objects.all().order_by('-order_date')[:5],
    }
    return render(request, 'finance/dashboard.html', context)

@login_required
def transaction_list(request):
    transactions = PurchaseOrder.objects.all().order_by('-order_date')
    context = {
        'transactions': transactions,
        'total_transactions': transactions.count(),
        'total_amount': transactions.aggregate(total=Sum('total_amount'))['total'] or 0,
    }
    return render(request, 'finance/transaction_list.html', context)
