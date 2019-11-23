from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Materia,Producto
from .forms import MateriaForm, MateriaAltForm, ProductoForm, ProductoAltForm
from apps.libro.models import Transaccion


def materialist(request):
    entradas= Materia.objects.filter(tipo=0)
    salidas = Materia.objects.filter(tipo=1)
    existencias = Materia.objects.filter(existencias__gt=0)
    form = MateriaForm()
    form2 = MateriaAltForm()
    contexto = {'entradas':entradas,'existencias':existencias,'salidas':salidas,'form':form,'form2':form2}
    return render(request,'inventario/material_list.html',contexto)


def entrada_create(request):
    if request.POST:
        form = MateriaForm(request.POST)
        post = form.save(commit=False)
        post.tipo = 0
        post.existencias = post.cantidad
        post.monto = post.cantidad * post.precio_unit
        post.save()
        messages.success(request,'ingreso de materia prima registrado correctamente!')
        return redirect('materia_list')
    else:
        form = MateriaForm()
    return redirect('materia_list')


def salida_create(request):
    if request.POST:
        materias= Materia.objects.filter(existencias__gt=0).filter(tipo=0)
        form = MateriaAltForm(request.POST)
        post = form.save(commit=False)
        remanente = post.cantidad
        post.cantidad = 0
        post.tipo =1
        i=0
        post.monto = 0
        acum = 0
        if materias:
            for materia in materias:
                if remanente < materia.existencias:
                    materia.existencias -= remanente
                    materia.monto = materia.existencias * materia.precio_unit
                    post.cantidad += remanente
                    remanente = 0
                    i+=1
                    post.monto += post.cantidad * materia.precio_unit
                    acum += float(materia.precio_unit)
                    materia.save()
                    break
                else:
                    if remanente > materia.existencias:
                        if materia.existencias > 0:
                            remanente -= materia.existencias
                            post.cantidad += materia.existencias
                            materia.existencias = 0
                            materia.monto =0
                            i+=1
                            acum += float(materia.precio_unit)
                            materia.save()
                    else:
                        if remanente == materia.existencias:
                            materia.existencias = 0
                            remanente = 0
                            i+=1
                            acum += float(materia.precio_unit)
                            materia.monto =0
                            materia.save()
                            break
            if remanente >0:
                messages.error(request, 'no existen suficientes unidades se despacho {} unidades y faltaron {}'.format(post.cantidad,remanente))
            if i != 0:
                post.existencias = 0
                post.precio_unit = float(acum)/i
                post.monto = int(post.cantidad) * post.precio_unit
                post.save()
        else:
            messages.error(request,'no existe materia prima para despachar')
        return redirect('materia_list')


def productolist(request):
    entradas= Producto.objects.filter(tipo=0)
    salidas = Producto.objects.filter(tipo=1)
    existencias = Producto.objects.filter(existencias__gt=0)
    form = ProductoForm()
    form2 = ProductoAltForm()
    contexto = {'entradas':entradas,'existencias':existencias,'salidas':salidas,'form':form,'form2':form2}
    return render(request,'inventario/producto_list.html',contexto)


def pentrada_create(request):
    if request.POST:
        form = ProductoForm(request.POST)
        post = form.save(commit=False)
        post.tipo = 0
        post.existencias = post.cantidad
        post.monto = post.cantidad * post.precio_unit
        post.save()
        messages.success(request,'ingreso producto registrado correctamente!')
        return redirect('producto_list')
    else:
        form = ProductoForm()
    return redirect('producto_list')


def psalida_create(request):
    if request.POST:
        materias= Producto.objects.filter(existencias__gt=0).filter(tipo=0)
        form = ProductoAltForm(request.POST)
        post = form.save(commit=False)
        remanente = post.cantidad
        post.cantidad = 0
        post.tipo =1
        i=0
        post.monto = 0
        acum = 0
        if materias:
            mat = materias.last()
            for materia in materias:
                if remanente < materia.existencias:
                    materia.existencias -= remanente
                    materia.monto = materia.existencias * materia.precio_unit
                    post.cantidad += remanente
                    remanente = 0
                    i+=1
                    post.monto += post.cantidad * materia.precio_unit
                    acum += float(materia.precio_unit)
                    materia.save()
                    break
                else:
                    if remanente > materia.existencias:
                        if materia.existencias > 0:
                            remanente -= materia.existencias
                            post.cantidad += materia.existencias
                            materia.existencias = 0
                            materia.monto =0
                            i+=1
                            acum += float(materia.precio_unit)
                            materia.save()
                    else:
                        if remanente == materia.existencias:
                            materia.existencias = 0
                            remanente = 0
                            i+=1
                            acum += float(materia.precio_unit)
                            materia.monto =0
                            materia.save()
                            break
            if remanente >0:
                messages.error(request, 'no existen suficientes unidades se despacho {} unidades y faltaron {}'.format(post.cantidad,remanente))
            if i != 0:
                post.existencias = 0
                post.precio_unit = float(acum)/i
                post.monto = int(post.cantidad) * post.precio_unit
                post.save()
        else:
            messages.error(request,'no existe producto para despachar ')
        return redirect('producto_list')

