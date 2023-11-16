from django import forms
from .models import Order, Route


# Formulario para Órdenes
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('ship_from', 'ship_to', 'commodity', 'value', 'volume', 'required_delivery_date', 'tax_percentage')
        widgets = {
            'ship_from': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Lugar de origen'}),
            'ship_to': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Lugar de destino'}),
            'commodity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mercancía'}),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Valor'}),
            'volume': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Volumen'}),
            'required_delivery_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Fecha de entrega requerida'}),
            'tax_percentage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Porcentaje de impuesto'}),
        }

class RouteForm(forms.ModelForm):
   class Meta:
       model = Route
       fields = [
           'source',
           'destination',
           'container_size',
           'carrier',
           'travel_mode',
           'extra_cost',
           'custom_clearance_time',
           'handling_time',
           'extra_time',
           'transit_time',
       ]
       widgets = {
           'source': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Lugar de origen'}),
           'destination': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Lugar de destino'}),
           'container_size': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Tamaño del Contenedor'}),
           'carrier': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Transportista'}),
           'travel_mode': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Modo de Viaje'}),
           'extra_cost': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Costo Extra'}),
           'custom_clearance_time': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Tiempo de Despacho Aduanero'}),
           'handling_time': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Tiempo de Manejo de Puerto/Aeropuerto/Estación de Tren'}),
           'extra_time': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Tiempo Extra'}),
           'transit_time': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Tiempo de Tránsito'}),
       }