from django import forms
from .models import Cuenta, SubCuenta


class CuentaForm(forms.ModelForm):
    class Meta:
        contexto = {'class': 'form-control', 'type': 'number', 'step': 'any', 'readonly': 'readonly'}
        contexto1 = {'class': 'form-control', 'type': 'number', 'step': 'any', 'readonly': 'readonly'}
        contexto2 = {'class': 'form-control', 'type': 'number', 'step': 'any', 'readonly': 'readonly'}
        model = Cuenta

        fields = [
            'nombre',
            'debe',
            'haber',
            'saldo',
            'rubro',
            'codigo',
        ]

        labels = {
            'nombre': 'nombre',
            'debe': 'debe $',
            'haber': 'haber $',
            'saldo': 'saldo $',
            'rubro': '',
            'codigo': '',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'debe': forms.TextInput(attrs=contexto1),
            'haber': forms.TextInput(attrs=contexto2),
            'saldo': forms.TextInput(attrs=contexto),
            'rubro': forms.Select(attrs={'class': 'form-control','hidden': 'hidden'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'hidden': 'hidden'}),
        }


class CuentaUForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ['nombre']
        labels = {'nombre':'nombre'}
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'})
        }


class SubCuentaForm(forms.ModelForm):

    class Meta:
        contexto = {'class': 'form-control', 'type': 'number', 'step': 'any', 'readonly': 'readonly'}
        model = SubCuenta

        fields = [
            'nombre',
            'debe',
            'haber',
            'saldo',
            'padre',
            'codigo',
        ]

        labels = {
            'nombre': 'nombre',
            'debe': 'debe $',
            'haber': 'haber $',
            'saldo': 'saldo $',
            'padre': '',
            'codigo': '',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'debe': forms.TextInput(attrs=contexto),
            'haber': forms.TextInput(attrs=contexto),
            'saldo': forms.TextInput(attrs=contexto),
            'padre': forms.Select(attrs={'class': 'form-control', 'hidden': 'hidden'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'hidden': 'hidden'}),
        }