from django.shortcuts import render, redirect
from django.db.models import Q
from apps.catalogo.models import SubCuenta, Cuenta
from apps.catalogo.functions import reset_subcuentas_now
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
            cargada.save()
            abonada.save()
            post.save()
            return redirect('index')
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
            cargada.save()
            abonada.save()
            post.save()
            return redirect('diario_list')
    else:
        contado = Cuenta.objects.get(codigo='1101')
        credito = Cuenta.objects.get(codigo='1102')
        abono1 = Cuenta.objects.get(codigo='1105')
        abono2 = Cuenta.objects.get(codigo='1201')
        form = VentaMixtaForm()
        form.fields['cargo'].queryset = SubCuenta.objects.all().filter(padre=contado)
        form.fields['cargo_alt'].queryset = SubCuenta.objects.all().filter(padre=credito)
        form.fields['abono'].queryset = SubCuenta.objects.all().filter(Q(padre=abono1) | Q(padre=abono2))
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


def gen_report(request):
    f_i = request.POST['f_inicio'] #formato 2019-11-01
    f_f = request.POST['f_fin']
    if request.POST:
        #filtroI = Transaccion.objects.filter(fecha__range=(f_i, f_f))  # <-- filtra rangos
        filtroF = Transaccion.objects.filter(fecha__lt=f_f)  # <--- filtra el valor previo

        ctas = reset_subcuentas_now()
        for T in filtroF:
            for ct in ctas:
                if T.tipo_transaccion == 0:
                    if ct == T.cargo:
                        ct.debe += float(T.monto)
                    else:
                        if ct == T.abono:
                            ct.abono += float(T.monto)
                else:
                    if T.tipo_transaccion ==1:
                        if ct == T.cargo:
                            ct.debe += float(T.monto_contado)
                        else:
                            if ct == T.cargo_alt:
                                ct.debe += float(T.monto_credito)
                            else:
                                if ct == T.abono:
                                    ct.haber += float(T.monto)
                    else:
                        if ct == T.cargo:
                            ct.debe += float(T.monto)
                        else:
                            if ct == T.abono:
                                ct.haber += float(T.monto_contado)
                            if ct == T.abono_alt:
                                ct.haber += float(T.monto_credito)
                ct.saldo = float(abs(ct.debe - ct.haber))
                print('valor inicial de {} {}'.format(ct.nombre,ct.saldo))
