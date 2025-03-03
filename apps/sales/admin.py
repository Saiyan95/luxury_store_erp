from django.contrib import admin
from .models import Sale, SaleItem

# Register your models here.

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    fields = ['product', 'quantity', 'unit_price', 'total_price']
    readonly_fields = ['total_price']

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['sale_number', 'customer_name', 'sale_date', 'total_amount', 'payment_method']
    list_filter = ['sale_date', 'payment_method']
    search_fields = ['sale_number', 'customer_name']
    inlines = [SaleItemInline]
    readonly_fields = ['created_by']
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by during the first save
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
