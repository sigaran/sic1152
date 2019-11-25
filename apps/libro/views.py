from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from apps.catalogo.models import SubCuenta, Cuenta, Rubro
from .models import Transaccion
from .forms import TransaccionForm, VentaMixtaForm, CompraMixtaForm


def createpdoble(request):
    ultimos = Transaccion.objects.all().order_by('-fecha')[:3][::-1]
    if request.POST:
        form = TransaccionForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            cargada = SubCuenta.objects.get(codigo=post.cargo.codigo)
            abonada = SubCuenta.objects.get(codigo=post.abono.codigo)
            cargada.debe += post.monto
            abonada.haber += post.monto
            cargada.saldo = float(abs(cargada.debe-cargada.haber))
            abonada.saldo = float(abs(abonada.debe - abonada.haber))
            cargada.save()
            abonada.save()
            post.save()
            return redirect('diario_list')
    else:
        form = TransaccionForm()
    contexto = {'form': form,'ultimos': ultimos}
    return render(request, 'libros/transaccion_form.html', contexto)


def venta_mixta(request):
    ultimos = Transaccion.objects.all().order_by('-fecha')[:3][::-1]
    if request.POST:
        form = VentaMixtaForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.tipo_transaccion = 1
            post.descripcion = 'venta mixta'
            cargada = SubCuenta.objects.get(codigo=post.cargo.codigo)
            cargada_alt = SubCuenta.objects.get(codigo=post.cargo_alt.codigo)
            abonada = SubCuenta.objects.get(codigo=post.abono.codigo)
            cargada.debe += post.monto_contado
            cargada_alt.debe += post.monto_credito
            post.monto = post.monto_credito + post.monto_contado
            abonada.haber += post.monto
            cargada.saldo = float(abs(cargada.debe - cargada.haber))
            cargada_alt.saldo = float(abs(cargada_alt.debe - cargada_alt.haber))
            abonada.saldo = float(abs(abonada.debe-abonada.haber))
            cargada_alt.save()
            cargada.save()
            abonada.save()
            post.save()
            return redirect('diario_list')
    else:
        contado = Cuenta.objects.get(codigo='1101')#EFECTIVO Y EQUIVALENTE
        credito = Cuenta.objects.get(codigo='1103')#CUENTAS Y DOCS POR COBRAR
        abono1 = Cuenta.objects.get(codigo='1104')#INVENTARIOS
        abono2 = Cuenta.objects.get(codigo='1201')#PROPIEDADES PLANTA Y EQ
        abono3 = Cuenta.objects.get(codigo='1202')  # PROPIEDADES PLANTA Y EQ
        abono4 = Cuenta.objects.get(codigo='5101')
        abono5 = Cuenta.objects.get(codigo='5102')
        form = VentaMixtaForm()
        form.fields['cargo'].queryset = SubCuenta.objects.all().filter(padre=contado)
        form.fields['cargo_alt'].queryset = SubCuenta.objects.all().filter(padre=credito)
        form.fields['abono'].queryset = SubCuenta.objects.all().filter(Q(padre=abono1) | Q(padre=abono2) | Q(padre=abono3) | Q(padre=abono4) | Q(padre=abono5))
    contexto = {'form': form, 'ultimos':ultimos}
    return render(request, 'libros/ventamixta_form.html', contexto)


def compra_mixta(request):
    ultimos = Transaccion.objects.all().order_by('-fecha')[:3][::-1]
    if request.POST:
        form = CompraMixtaForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.tipo_transaccion = 2
            post.descripcion = 'compra mixta'
            cargada = SubCuenta.objects.get(codigo=post.cargo.codigo)
            abonada = SubCuenta.objects.get(codigo=post.abono.codigo)
            abonada_alt = SubCuenta.objects.get(codigo=post.abono_alt.codigo)
            abonada.haber += post.monto_contado
            abonada_alt.haber += post.monto_credito
            post.monto = post.monto_credito + post.monto_contado
            cargada.debe += post.monto
            cargada.saldo += float(abs(cargada.debe - cargada.haber))
            abonada.saldo += float(abs(abonada.debe - abonada.haber))
            abonada_alt.saldo += float(abs(abonada_alt.debe - abonada_alt.haber))
            abonada_alt.save()
            cargada.save()
            abonada.save()
            post.save()
            return redirect('diario_list')
    else:
        contado = Cuenta.objects.get(codigo='1101')
        credito = Cuenta.objects.get(codigo='2101')
        abono1 = Cuenta.objects.get(codigo='1105')
        abono2 = Cuenta.objects.get(codigo='1201')
        form = CompraMixtaForm()
        form.fields['abono'].queryset = SubCuenta.objects.all().filter(padre=contado)
        form.fields['abono_alt'].queryset = SubCuenta.objects.all().filter(padre=credito)
        form.fields['cargo'].queryset = SubCuenta.objects.all().filter(Q(padre=abono1) | Q(padre=abono2))
    contexto = {'form': form, 'ultimos':ultimos}
    return render(request, 'libros/compramixta_form.html', contexto)


def diariolist(request):
    ultimos = Transaccion.objects.all().order_by('-fecha')[:3][::-1]
    transacciones = Transaccion.objects.all()
    contexto = {'trans': transacciones,'ultimos':ultimos}
    return render(request, 'libros/diario_list.html', contexto)

