from django import forms
from apps.planilla.models import Empleado


class EmpleadoForm(forms.ModelForm):
    class Meta:
        html = {'class': 'form-control text-gray-900 '}
        model = Empleado
        fields = [
            'nombres',
            'puesto',
            'fecha',
            'codigo',
            'salario',
            'desc',
        ]

        labels = {
            'nombres': 'nombres',
            'puesto': 'puesto',
            'fecha':'fecha',
            'codigo': 'codigo',
            'salario': 'salario',
            'desc':'otros descuentos',
        }

        widgets = {
            'nombres': forms.TextInput(attrs=html),
            'puesto': forms.TextInput(attrs=html),
            'fecha': forms.TextInput(attrs={'class': 'form-control text-gray-900 ', 'placeholder': '2019-12-31'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control text-gray-900 ', 'placeholder': 'EMP000000'}),
            'salario': forms.TextInput(attrs=html),
            'desc': forms.TextInput(attrs={'class': 'form-control text-gray-900 ','type': 'number','step': 'any'})

        }


class EmpleadoUForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = [
            'nombres',
            'puesto',
            'codigo',
            'salario',
            'desc',
        ]

        labels = {
            'nombres': 'nombres',
            'puesto': 'puesto',
            'codigo': 'codigo',
            'salario': 'salario',
            'desc':'otros descuentos',
        }

        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'puesto': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'salario': forms.TextInput(attrs={'class': 'form-control','type':'number','step':'any'}),
            'desc': forms.TextInput(attrs={'class':'form-control','type':'number','step':'any'})
        }
