from django import forms
from apps.planilla.models import Empleado


class EmpleadoForm(forms.ModelForm):
    class Meta:
        html = {'class': 'form-control text-gray-900 '}
        model = Empleado
        fields = [
            'nombres',
            'apellidos',
            'codigo',
            'salario',
        ]

        labels = {
            'nombres': 'nombres',
            'apellidos': 'apellidos',
            'codigo': 'codigo',
            'salario': 'salario',
        }

        widgets = {
            'nombres': forms.TextInput(attrs=html),
            'apellidos': forms.TextInput(attrs=html),
            'codigo': forms.TextInput(attrs={'class': 'form-control text-gray-900 ', 'placeholder': 'EMP000000'}),
            'salario': forms.TextInput(attrs=html),
        }


class EmpleadoUForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = [
            'nombres',
            'apellidos',
            'codigo',
            'salario',
        ]

        labels = {
            'nombres': 'nombres',
            'apellidos': 'apellidos',
            'codigo': 'codigo',
            'salario': 'salario',
        }

        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'salario': forms.TextInput(attrs={'class': 'form-control'}),
        }
