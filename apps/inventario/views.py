from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Materia
from .forms import MateriaForm, MateriaAltForm
#from apps.libro.models import Transaccion


def materialist(request):
    materiales = Materia.objects.all()
    form = MateriaForm()
    form2 = MateriaAltForm()
    return render(request,'inventario/material_list.html',{'materiales':materiales,'form':form,'form2':form2})


def entrada_create(request):
    if request.POST:
        form = MateriaForm(request.POST)
        post = form.save(commit=False)
        post.tipo = 0
        post.monto = post.cantidad * post.precio_unit
        post.save()
        return redirect('materia_list')
    else:
        form = MateriaForm()
    return redirect('materia_list')


def salida_create(request):
    if request.POST:
        materias= Materia.objects.filter(tipo=0)
        form = MateriaAltForm(request.POST)
        post = form.save(commit=False)
        remanente = post.cantidad
        post.tipo =1
        i=0
        post.monto = 0
        acum = 0
        for materia in materias:
            if remanente < materia.cantidad:
                materia.cantidad -= remanente
                materia.monto = materia.cantidad * materia.precio_unit
                remanente = 0
                i+=1
                post.monto += remanente * materia.precio_unit
                acum += float(materia.precio_unit)
                materia.save()
                break
            else:
                if remanente > materia.cantidad:
                    remanente -= materia.cantidad
                    post.monto += materia.cantidad * materia.precio_unit
                    materia.cantidad =0
                    materia.monto =0
                    i+=1
                    acum += float(materia.precio_unit)
                    materia.save()
                else:
                    if remanente == materia.cantidad:
                        materia.cantidad = 0
                        remanente = 0
                        post.monto =remanente * materia.precio_unit
                        i+=1
                        acum += float(materia.precio_unit)
                        materia.monto =0
                        materia.save()
                        break
        post.precio_unit = float(acum)/i
        post.monto = int(post.cantidad) * post.precio_unit
        post.save()
        return redirect('materia_list')
    else:
        form = MateriaAltForm()
    return redirect('materia_list')
