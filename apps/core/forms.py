from django import forms
from .models import Order


# Formulario para Órdenes
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('ship_from', 'ship_to', 'commodity', 'value', 'volume', 'required_delivery_date', 'tax_percentage')
        widgets = {
            'ship_from': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Lugar de origen'}),
            'ship_to': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Lugar de destino'}),
            'commodity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mercancía'}),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Valor'}),
            'volume': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Volumen'}),
            'required_delivery_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Fecha de entrega requerida'}),
            'tax_percentage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Porcentaje de impuesto'}),
        }
