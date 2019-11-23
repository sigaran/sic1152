import csv, io
from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView
from apps.planilla.forms import EmpleadoForm, EmpleadoUForm
from apps.planilla.models import Empleado
from apps.libro.models import Transaccion


class EmpleadoList(ListView):
    ultimos = Transaccion.objects.all().order_by('-fecha')[:3][::-1]
    model = Empleado
    extra_context = {'ultimos': ultimos}
    template_name = 'planilla/empleado_list.html'


def empleadocreate(request):
    ultimos = Transaccion.objects.all().order_by('-fecha')[:3][::-1]
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.renta = post.salario * 0.08
            post.isss = post.salario * 0.025
            post.afp = post.salario * 0.07
            subtotal = post.afp + post.isss + post.renta
            post.sal_neto = post.salario - subtotal
            messages.success(request,'empleado {} añadido correctamente'.format(post.nombres))
            post.save()
            return redirect('empleado_list')
    else:
        form = EmpleadoForm()
    return render(request, 'planilla/empleado_form.html', {'form': form,'ultimos':ultimos})


def empleadoupdate(request, pk):
    empleado = Empleado.objects.get(codigo=pk)
    if request.method == 'GET':
        form = EmpleadoUForm(instance=empleado)
    else:
        form = EmpleadoUForm(request.POST, instance=empleado)
        if form.is_valid():
            post = form.save(commit=False)
            post.renta = post.salario * 0.08
            post.isss = post.salario * 0.025
            post.afp = post.salario * 0.07
            subtotal = post.afp + post.isss + post.renta
            post.sal_neto = post.salario - subtotal
            post.save()
            messages.success(request,'datos del empleado {} modificados correctamente'.format(post.nombres))
            return redirect('empleado_list')
    return render(request, 'planilla/empleado_form.html', {'form': form})


def planilla_import(request):

    if request.POST:
        try:
            csv_file = request.FILES['file']
        except MultiValueDictKeyError:
            return render(request, 'planilla/planilla_error.html')
        try:
            dataset = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(dataset)
            next(io_string)
            for colum in csv.reader(io_string, delimiter=','):
                created = Empleado.objects.update_or_create(
                    codigo=colum[0],
                    nombres=colum[1],
                    apellidos=colum[2],
                    salario=colum[3],
                    isss=colum[4],
                    renta=colum[5],
                    afp=colum[6],
                    sal_neto=colum[7]
                )
        except ValueError or IndexError or StopIteration or UnicodeDecodeError:
            ultimos = Transaccion.objects.all().order_by('-fecha')[:3][::-1]
            return render(request, 'planilla/planilla_error.html',{'ultimos':ultimos})
        messages.success(request,'planilla actualizada con exito')
        return redirect('empleado_list')
    else:
        return redirect('empleado_list')