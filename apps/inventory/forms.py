from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'sku', 'category', 'brand', 'description', 'cost_price', 'quantity', 'reorder_point', 'image', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'cost_price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'quantity': forms.NumberInput(attrs={'min': '0'}),
            'reorder_point': forms.NumberInput(attrs={'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'image':
                self.fields[field].widget.attrs.update({'class': 'form-control'})
            else:
                self.fields[field].widget.attrs.update({'class': 'form-control-file'})
