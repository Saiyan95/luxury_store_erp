from django import forms
from .models import Sale, SaleItem
from apps.inventory.models import Product

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['sale_number', 'customer_name', 'payment_method', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['product', 'quantity', 'unit_price']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': '1', 'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(is_active=True, quantity__gt=0)
        self.fields['product'].widget.attrs.update({'class': 'form-control'})

SaleItemFormSet = forms.inlineformset_factory(
    Sale, SaleItem,
    form=SaleItemForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
)
