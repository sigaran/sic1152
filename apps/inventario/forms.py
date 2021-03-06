from django import forms
from .models import Materia, Producto


class MateriaForm(forms.ModelForm):
    class Meta:
        args_fecha = {'class': 'form-control', 'data-provide': 'datepicker'}
        model = Materia
        fields = [
            'cantidad',
            'precio_unit',
        ]
        labels = {
            'cantidad': 'cantidad',
            'precio_unit': 'precio unitario'
        }
        widgets = {
            'cantidad': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}),
            'precio_unit': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'step': 'any'})
        }


class MateriaAltForm(forms.ModelForm):
    class Meta:
        args_fecha = {'class': 'form-control', 'data-provide': 'datepicker'}
        model = Materia
        fields = [
            'cantidad',
        ]
        labels = {
            'cantidad': 'cantidad',
        }
        widgets = {
            'cantidad': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}),
        }


class ProductoForm(forms.ModelForm):
    class Meta:
        args_fecha = {'class': 'form-control', 'data-provide': 'datepicker'}
        model = Producto
        fields = [
            'cantidad',
            'precio_unit',
        ]
        labels = {
            'cantidad': 'cantidad',
            'precio_unit': 'precio unitario'
        }
        widgets = {
            'cantidad': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}),
            'precio_unit': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'step': 'any'})
        }


class ProductoAltForm(forms.ModelForm):
    class Meta:
        args_fecha = {'class': 'form-control', 'data-provide': 'datepicker'}
        model = Producto
        fields = [
            'cantidad',
        ]
        labels = {
            'cantidad': 'cantidad',
        }
        widgets = {
            'cantidad': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}),
        }
