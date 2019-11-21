from django import forms
from .models import Transaccion


class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = [
            'descripcion',
            'cargo',
            'descripcion_cargo',
            'abono',
            'descripcion_abono',
            'monto',
        ]
        labels = {
            'descripcion': 'descripcion de la transaccion',
            'cargo': 'cargo',
            'descripcion_cargo': 'descripcion de cargo',
            'abono': 'abono',
            'descripcion_abono': 'descripcion de abono',
            'monto': 'monto de la transaccion:'
        }
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'cargo': forms.Select(attrs={'class': 'form-control mb-2'}),
            'descripcion_cargo': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'abono': forms.Select(attrs={'class': 'form-control mb-2'}),
            'descripcion_abono': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'monto': forms.TextInput(attrs={'class': 'form-control mb-2', 'type': 'number', 'steps': 'any'})
        }


class VentaMixtaForm(forms.ModelForm):
    class Meta:
        estilo = {'class': 'form-control mb-2', 'type': 'number', 'steps': 'any'}
        model = Transaccion
        fields = [
            'cargo',
            'monto_contado',
            'cargo_alt',
            'monto_credito',
            'descripcion_cargo',
            'abono',
            'descripcion_abono',
        ]
        labels = {
            'cargo': 'metodo  de pago contado',
            'monto_contado': 'monto al contado',
            'cargo_alt': 'metodo de pago credito',
            'monto_credito': 'monto al credito',
            'descripcion_cargo': 'descripcion del cargo',
            'abono': 'abono',
            'descripcion_abono':'descripcion del abono'
        }
        widgets = {
            'cargo': forms.Select(attrs={'class': 'form-control mb-2'}),
            'monto_contado': forms.TextInput(attrs=estilo),
            'cargo_alt': forms.Select(attrs={'class': 'form-control mb-2'}),
            'monto_credito': forms.TextInput(attrs=estilo),
            'descripcion_cargo': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'abono': forms.Select(attrs={'class': 'form-control mb-2'}),
            'descripcion_abono': forms.TextInput(attrs={'class': 'form-control mb-2'}),
        }


class CompraMixtaForm(forms.ModelForm):
    class Meta:
        estilo = {'class': 'form-control mb-2', 'type': 'number', 'steps': 'any'}
        model = Transaccion
        fields = [
            'abono',
            'monto_contado',
            'abono_alt',
            'monto_credito',
            'descripcion_abono',
            'cargo',
            'descripcion_cargo',
        ]
        labels = {
            'abono': 'metodo  de pago contado',
            'monto_contado': 'monto al contado',
            'abono_alt': 'metodo de pago credito',
            'monto_credito': 'monto al credito',
            'descripcion_abono': 'descripcion del abono',
            'cargo': 'cargo',
            'descripcion_cargo':'descripcion del cargo'
        }
        widgets = {
            'abono': forms.Select(attrs={'class': 'form-control mb-2'}),
            'monto_contado': forms.TextInput(attrs=estilo),
            'abono_alt': forms.Select(attrs={'class': 'form-control mb-2'}),
            'monto_credito': forms.TextInput(attrs=estilo),
            'descripcion_abono': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'cargo': forms.Select(attrs={'class': 'form-control mb-2'}),
            'descripcion_cargo': forms.TextInput(attrs={'class': 'form-control mb-2'}),
        }
