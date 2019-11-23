from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView,UpdateView
from .models import Cuenta, SubCuenta, Tipo, Rubro
from .functions import update_cuentas_now
from .forms import CuentaForm, SubCuentaForm, CuentaUForm
from apps.libro.models import Transaccion

import time
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse


class Search_Ct(TemplateView):

    def post(self, request):
        ultimos = Transaccion.objects.all().order_by('-fecha')[:3][::-1]
        buscar = request.POST['buscar']
        tipos_c = Tipo.objects.all().filter(codigo=buscar)
        tipos_n = Tipo.objects.all().filter(nombre__contains=buscar)
        rubros = Rubro.objects.all()
        cuentas = Cuenta.objects.all()
        subcuentas = SubCuenta.objects.all()
        if tipos_c:
            contexto = {'tipos': tipos_c,'rubros': rubros,'cuentas': cuentas,'subcuentas':subcuentas,'ultimos':ultimos}
            return render(request, 'catalogo/cuentas_list.html', contexto)
        else:
            if buscar == 'cuentas':
                tipos = Tipo.objects.all().filter(nombre=buscar)
                rubros = Rubro.objects.all().filter(nombre=buscar)
                cuentas = Cuenta.objects.all()
                subcuentas = SubCuenta.objects.all().filter(nombre=buscar)
                contexto = {'tipos': tipos,'rubros':rubros,'cuentas':cuentas,'subcuentas':subcuentas,'ultimos':ultimos}
                return render(request, 'base/index.html', contexto)
            else:
                if buscar == 'subcuentas':
                    tipos = Tipo.objects.all().filter(nombre=buscar)
                    rubros = Rubro.objects.all().filter(nombre=buscar)
                    cuentas = Cuenta.objects.all().filter(nombre=buscar)
                    subcuentas = SubCuenta.objects.all()
                    contexto = {'tipos': tipos,'rubros':rubros,'cuentas':cuentas,'subcuentas':subcuentas,'ultimos':ultimos}
                    return render(request, 'base/index.html', contexto)
                else:
                    if buscar == 'rubros':
                        tipos = Tipo.objects.all().filter(nombre=buscar)
                        rubros = Rubro.objects.all()
                        cuentas = Cuenta.objects.all().filter(nombre=buscar)
                        subcuentas = SubCuenta.objects.all().filter(nombre=buscar)
                        contexto = {'tipos': tipos, 'rubros': rubros, 'cuentas': cuentas, 'subcuentas': subcuentas,'ultimos':ultimos}
                        return render(request, 'base/index.html', contexto)
                    else:
                        if tipos_n:
                            contexto = {'tipos': tipos_n, 'rubros': rubros, 'cuentas': cuentas, 'subcuentas': subcuentas,'ultimos':ultimos}
                            return render(request, 'catalogo/cuentas_list.html', contexto)
                        else:
                            return redirect('404')


def cuentacreate(request, pk):
    ultimos = Transaccion.objects.all().order_by('-fecha')[:3][::-1]
    rubro = Rubro.objects.get(codigo=pk)
    cuentas = Cuenta.objects.all().filter(rubro=rubro)
    maximo = Cuenta.objects.all().filter(rubro=rubro).last()
    if maximo:
        recomendado = int(maximo.codigo) + 1
    else:
        recomendado = (int(rubro.codigo) * 100) + 1
    if request.POST:
        form = CuentaForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.rubro = rubro
            post.codigo = recomendado.__str__()
            post.save()
            return redirect('cuenta_list')
    else:
        form = CuentaForm()
    contexto = {'form': form, 'rubro': rubro, 'cuentas': cuentas, 'ultimo': maximo, 'recomendado': recomendado,'ultimos':ultimos}
    return render(request, 'catalogo/cuenta_form.html', contexto)


def subcuentacreate(request, pk):
    ultimos = Transaccion.objects.all().order_by('-fecha')[:3][::-1]
    cuenta = Cuenta.objects.get(codigo=pk)
    subcuentas = SubCuenta.objects.all().filter(padre=cuenta)
    maximo = SubCuenta.objects.all().filter(padre=cuenta).last()
    if maximo:
        recomendado = int(maximo.codigo) + 1
    else:
        recomendado = (int(cuenta.codigo) * 100) + 1
    if request.POST:
        form = SubCuentaForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.padre = cuenta
            post.codigo = recomendado.__str__()
            post.save()
            update_cuentas_now()
            return redirect('cuenta_list')
    else:
        form = SubCuentaForm()
    contexto = {'form': form, 'cuenta': cuenta, 'subcuentas': subcuentas, 'ultimo': maximo, 'recomentado': recomendado,'ultimos':ultimos}
    return render(request, 'catalogo/subcuenta_form.html', contexto)


def cuentalist(request):
    ultimos = Transaccion.objects.all().order_by('-fecha')[:3][::-1]
    #update_cuentas_now()
    form = CuentaUForm
    tipo = Tipo.objects.all()
    rubro = Rubro.objects.all()
    cuenta = Cuenta.objects.all()
    subcuenta = SubCuenta.objects.all()
    contexto = {'cuentas': cuenta, 'subcuentas': subcuenta, 'tipos': tipo, 'rubros': rubro, 'form': form,'ultimos':ultimos}
    return render(request, 'catalogo/cuentas_list.html', contexto)


def catalogo_report(request):
    tipos = Tipo.objects.all()
    rubros = Rubro.objects.all()
    cuentas = Cuenta.objects.all()
    subcuentas = SubCuenta.objects.all()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=catalogo.pdf'
    buffer = BytesIO()
    cv = canvas.Canvas(buffer, pagesize=A4)

    cv.setLineWidth(.3)
    cv.setFont('Helvetica-Bold', 22)
    cv.drawString(30, 750, 'CATALOGO DE CUENTAS')
    cv.setFont('Helvetica', 12)
    cv.drawString(30, 735, '{} {}'.format('Ejercicio', time.strftime("%Y")))
    cv.setFont('Helvetica-Bold', 12)
    cv.drawString(480, 750, 'SIC115')
    cv.setFont('Helvetica-Bold', 12)
    cv.drawString(30, 720, 'codigo')
    cv.drawString(120, 720, 'nombre')
    cv.drawString(450, 720, 'saldo')
    b = 720
    b -= 15
    conteo = 0

    cv.setFillColorRGB(0.92578125, 0.92578125, 0.92578125)
    cv.setStrokeColorRGB(0.92578125, 0.92578125, 0.92578125)
    cv.setFont('Helvetica-Bold', 42)
    cv.line(130, 443, 450, 443, )
    cv.line(130, 442, 450, 442, )
    cv.drawString(130, 400, 'CONFIDENCIAL')
    cv.line(130, 390, 450, 390, )
    cv.line(130, 389, 450, 389, )
    cv.setFillColorRGB(0, 0, 0)

    for tipo in tipos:
        if conteo == 44:
            cv.showPage()
            conteo = 0
            cv.setFont('Helvetica-Bold', 12)
            cv.drawString(30, 750, 'codigo')
            cv.drawString(120, 750, 'nombre')
            cv.drawString(450, 750, 'saldo')
            cv.setFillColorRGB(0.92578125, 0.92578125, 0.92578125)
            cv.setStrokeColorRGB(0.92578125, 0.92578125, 0.92578125)
            cv.setFont('Helvetica-Bold', 42)
            cv.line(130, 443, 450, 443, )
            cv.line(130, 442, 450, 442, )
            cv.drawString(130, 400, 'CONFIDENCIAL')
            cv.line(130, 390, 450, 390, )
            cv.line(130, 389, 450, 389, )
            cv.setFillColorRGB(0, 0, 0)
            b = 735
        cv.setFont('Helvetica', 12)
        cv.drawString(40, b, tipo.codigo)
        cv.drawString(130, b, tipo.nombre)
        cv.drawString(460, b, tipo.saldo.__str__())
        b -= 15
        conteo += 1
        for rubro in rubros:
            if conteo == 44:
                cv.showPage()
                conteo = 0
                cv.setFont('Helvetica-Bold', 12)
                cv.drawString(30, 750, 'codigo')
                cv.drawString(120, 750, 'nombre')
                cv.drawString(450, 750, 'saldo')
                cv.setFillColorRGB(0.92578125, 0.92578125, 0.92578125)
                cv.setStrokeColorRGB(0.92578125, 0.92578125, 0.92578125)
                cv.setFont('Helvetica-Bold', 42)
                cv.line(130, 443, 450, 443, )
                cv.line(130, 442, 450, 442, )
                cv.drawString(130, 400, 'CONFIDENCIAL')
                cv.line(130, 390, 450, 390, )
                cv.line(130, 389, 450, 389, )
                cv.setFillColorRGB(0, 0, 0)
                b = 735
            if rubro.tipo == tipo:
                cv.setFont('Helvetica', 12)
                cv.drawString(50, b, rubro.codigo)
                cv.drawString(140, b, rubro.nombre)
                cv.drawString(460, b, rubro.saldo.__str__())
                b -= 15
                conteo += 1
                for cuenta in cuentas:
                    if conteo == 44:
                        cv.showPage()
                        conteo = 0
                        cv.setFont('Helvetica-Bold', 12)
                        cv.drawString(30, 750, 'codigo')
                        cv.drawString(120, 750, 'nombre')
                        cv.drawString(450, 750, 'saldo')
                        cv.setFillColorRGB(0.92578125, 0.92578125, 0.92578125)
                        cv.setStrokeColorRGB(0.92578125, 0.92578125, 0.92578125)
                        cv.setFont('Helvetica-Bold', 42)
                        cv.line(130, 443, 450, 443, )
                        cv.line(130, 442, 450, 442, )
                        cv.drawString(130, 400, 'CONFIDENCIAL')
                        cv.line(130, 390, 450, 390, )
                        cv.line(130, 389, 450, 389, )
                        cv.setFillColorRGB(0, 0, 0)
                        b = 735
                    if cuenta.rubro == rubro:
                        cv.setFont('Helvetica', 12)
                        cv.drawString(60, b, cuenta.codigo)
                        cv.drawString(150, b, cuenta.nombre)
                        cv.drawString(460, b, cuenta.saldo.__str__())
                        b -= 15
                        conteo += 1
                        for subcuenta in subcuentas:
                            if conteo == 44:
                                cv.showPage()
                                conteo = 0
                                cv.setFont('Helvetica-Bold', 12)
                                cv.drawString(30, 750, 'codigo')
                                cv.drawString(120, 750, 'nombre')
                                cv.drawString(450, 750, 'saldo')
                                cv.setFillColorRGB(0.92578125, 0.92578125, 0.92578125)
                                cv.setStrokeColorRGB(0.92578125, 0.92578125, 0.92578125)
                                cv.setFont('Helvetica-Bold', 42)
                                cv.line(130, 443, 450, 443, )
                                cv.line(130, 442, 450, 442, )
                                cv.drawString(130, 400, 'CONFIDENCIAL')
                                cv.line(130, 390, 450, 390, )
                                cv.line(130, 389, 450, 389, )
                                cv.setFillColorRGB(0, 0, 0)
                                b = 735
                            if subcuenta.padre == cuenta:
                                cv.setFont('Helvetica', 12)
                                cv.drawString(70, b, subcuenta.codigo)
                                cv.drawString(160, b, subcuenta.nombre)
                                cv.drawString(460, b, subcuenta.saldo.__str__())
                                b -= 15
                                conteo += 1
    cv.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def cuentaupdate(request, pk):
    cuenta = Cuenta.objects.get(codigo=pk)
    if request.POST:
        cuenta.nombre = request.POST['nombre']
        cuenta.save()
        return redirect('cuenta_list')


def subcuentaupdate(request, pk):
    subcuenta = SubCuenta.objects.get(codigo=pk)
    if request.POST:
        subcuenta.nombre = request.POST['nombre']
        subcuenta.save()
        return redirect('cuenta_list')
