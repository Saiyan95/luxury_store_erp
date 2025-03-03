from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Sale, SaleItem
from .forms import SaleForm, SaleItemFormSet
from django.db.models import Sum, F

# Create your views here.

@login_required
def add_sale(request):
    if request.method == 'POST':
        sale_form = SaleForm(request.POST)
        if sale_form.is_valid():
            with transaction.atomic():
                sale = sale_form.save(commit=False)
                sale.created_by = request.user
                sale.save()
                
                formset = SaleItemFormSet(request.POST, instance=sale)
                if formset.is_valid():
                    # Calculate total amount
                    total_amount = 0
                    for form in formset:
                        if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                            sale_item = form.save(commit=False)
                            sale_item.total_price = sale_item.quantity * sale_item.unit_price
                            total_amount += sale_item.total_price
                            
                            # Update product quantity
                            product = sale_item.product
                            if product.quantity >= sale_item.quantity:
                                product.quantity -= sale_item.quantity
                                product.save()
                            else:
                                raise ValueError(f"Insufficient stock for {product.name}")
                            
                            sale_item.save()
                    
                    sale.total_amount = total_amount
                    sale.save()
                    
                    messages.success(request, f'Sale {sale.sale_number} has been created successfully.')
                    return redirect('sales_dashboard')
    else:
        sale_form = SaleForm()
        formset = SaleItemFormSet()
    
    context = {
        'sale_form': sale_form,
        'formset': formset,
        'title': 'New Sale',
    }
    return render(request, 'sales/sale_form.html', context)

@login_required
def sales_list(request):
    sales = Sale.objects.all().order_by('-sale_date')
    total_sales = sales.count()
    total_revenue = sales.aggregate(total=Sum('total_amount'))['total'] or 0
    
    context = {
        'sales': sales,
        'total_sales': total_sales,
        'total_revenue': total_revenue,
    }
    return render(request, 'sales/sales_list.html', context)
