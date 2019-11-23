from django.contrib import messages
from django.shortcuts import render, redirect
from apps.catalogo.models import Tipo, Rubro
from apps.libro.models import Transaccion
from .forms import RegisterForm

import time
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse


def diario_report(request):

    if request.POST:
        f_i = request.POST['inicio']
        f_f = request.POST['fin']
        query = Transaccion.objects.filter(fecha__range=(f_i,f_f))
        if query:
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=clasificacion_general.pdf'
            buffer = BytesIO()
            cv = canvas.Canvas(buffer, pagesize=A4)
            cv.setFont('Helvetica-Bold', 12)
            cv.drawString(30,750,'EMPRESA PLASTINOSEQUE')
            cv.drawString(30,725,'registro de transacciones del {} al {}'.format(f_i,f_f))
            a=30
            b=715
            c=260
            d=460
            conteo =0
            for T in query:
                if conteo == 44:
                    cv.showPage()
                    conteo = 0
                    cv.setFont('Helvetica-Bold', 12)
                    cv.drawString(30, 750, 'fecha')
                    cv.drawString(120, 750, 'descripcion')
                    cv.drawString(450, 750, 'monto')
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
                cv.drawString(a,b,T.fecha.__str__())
                cv.drawString(c,b,T.descripcion)
                cv.drawString(d,b,T.monto.__str__())
                b -=25
                conteo +=1
            fecha = time.strftime("%d/%m/%y")
            hora = time.strftime("%H:%M:%S")
            string = '{} {} {} {} {} {}'.format('reporte generado por ', request.user.username, 'el', fecha,' a las ',hora)
            cv.drawString(30, 30, string)
            cv.setFillColorRGB(0.92578125, 0.92578125, 0.92578125)
            cv.setStrokeColorRGB(0.92578125, 0.92578125, 0.92578125)
            cv.setFont('Helvetica-Bold', 42)
            cv.line(130, 443, 450, 443, )
            cv.line(130, 442, 450, 442, )
            cv.drawString(130, 400, 'CONFIDENCIAL')
            cv.line(130, 390, 450, 390, )
            cv.line(130, 389, 450, 389, )
            cv.save()
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            return response
        else:
            messages.error(request,'no se encontraron transacciones para el periodo del {} al {}'.format(f_i,f_f))
            return redirect('report_index')


def tipos_repot(request):
    tipos = Tipo.objects.all()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=clasificacion_general.pdf'

    buffer = BytesIO()
    cv = canvas.Canvas(buffer, pagesize=A4)
    # generacion de encabezados del pdf
    # dragString(px izq a derecha, px de abajo hacia arriba, string que queremos dibujar)
    cv.setLineWidth(.3)
    cv.setFont('Helvetica-Bold', 22)
    cv.drawString(30, 750, 'SIC115 Reporte')
    cv.setFont('Helvetica', 12)
    cv.drawString(30, 735, 'Clasificacion General')
    cv.setFont('Helvetica-Bold', 12)
    cv.drawString(480, 750, 'aqui puede ir algo ')
    cv.setFont('Helvetica-Bold', 12)
    cv.drawString(480, 735, 'aqui tambien xd')

    # generando contenido del pdf
    a = 30
    b = 645
    c = 390
    d = 460
    cv.setFont('Helvetica-Bold', 14)
    cv.drawString(a, b, 'nombre')
    cv.setFont('Helvetica-Bold', 14)
    cv.drawString(c, b, 'saldo')
    cv.setFont('Helvetica-Bold', 14)
    cv.drawString(d, b, 'tipo de saldo')
    b -= 25
    c += 10
    d += 10
    # marca de agua
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
        cv.setFont('Helvetica', 12)
        cv.drawString(a, b, tipo.nombre.__str__())
        cv.setFont('Helvetica', 12)
        cv.drawString(c, b, tipo.saldo.__str__())
        if tipo.debe > tipo.haber:
            cv.setFont('Helvetica', 12)
            cv.drawString(d, b, 'saldo deudor')
        else:
            if tipo.debe < tipo.haber:
                cv.setFont('Helvetica', 12)
                cv.drawString(d, b, 'saldo acreedor')
            else:
                cv.setFont('Helvetica', 12)
                cv.drawString(d, b, 'saldo cero')
        b -= 25
    cv.setFont('Helvetica', 12)
    fecha =  time.strftime("%d/%m/%y")
    hora = time.strftime("%H:%M:%S")
    cv.drawString(30, 30, '{} {} {} {} {} {}'.format('reporte generado por ', request.user.username, 'el', fecha, ' a las ', hora))
    cv.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def index(request):
    tipos = Tipo.objects.all()
    ultimos = Transaccion.objects.all().order_by('-fecha')[:3][::-1]
    return render(request, 'base/index.html', {'tipos': tipos,'ultimos':ultimos})


def error_404(request):
    ultimos = Transaccion.objects.all().order_by('-fecha')[:3][::-1]

    return render(request, 'errors/404.html',{'ultimos':ultimos})


def support(request):
    return render(request, 'base/support.html')


def usercreate(request):
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            if post.is_staff:
                post.is_superuser = True
            post.save()
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'base/registrar.html', {'form': form})


def report_index(request):
    fecha = time.strftime("%d/%m/%y")
    return render(request, 'reportes.html',{'fecha':fecha})


def rubros_repot(request):
    rubros = Rubro.objects.all()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=rubros_agrupacion.pdf'

    buffer = BytesIO()
    cv = canvas.Canvas(buffer, pagesize=A4)
    # generacion de encabezados del pdf
    # dragString(px izq a derecha, px de abajo hacia arriba, string que queremos dibujar)
    cv.setLineWidth(.3)
    cv.setFont('Helvetica-Bold', 22)
    cv.drawString(30, 750, 'SIC115 Reporte')
    cv.setFont('Helvetica', 12)
    cv.drawString(30, 735, 'Rubros de Agrupacion')
    cv.setFont('Helvetica-Bold', 12)
    cv.drawString(480, 750, 'aqui puede ir algo ')
    cv.setFont('Helvetica-Bold', 12)
    cv.drawString(480, 735, 'aqui tambien xd')

    # generando contenido del pdf
    a = 30
    b = 645
    c = 390
    d = 460
    cv.setFont('Helvetica-Bold', 14)
    cv.drawString(a, b, 'nombre')
    cv.setFont('Helvetica-Bold', 14)
    cv.drawString(c, b, 'saldo')
    cv.setFont('Helvetica-Bold', 14)
    cv.drawString(d, b, 'tipo de saldo')
    b -= 25
    c += 10
    d += 10
    cv.setFillColorRGB(0.92578125, 0.92578125, 0.92578125)
    cv.setStrokeColorRGB(0.92578125, 0.92578125, 0.92578125)
    cv.setFont('Helvetica-Bold', 42)
    cv.line(130, 443, 450, 443, )
    cv.line(130, 442, 450, 442, )
    cv.drawString(130, 400, 'CONFIDENCIAL')
    cv.line(130, 390, 450, 390, )
    cv.line(130, 389, 450, 389, )

    cv.setFillColorRGB(0, 0, 0)
    for rubro in rubros:
        cv.setFont('Helvetica', 12)
        cv.drawString(a, b, rubro.nombre.__str__())
        cv.setFont('Helvetica', 12)
        cv.drawString(c, b, rubro.saldo.__str__())
        if rubro.debe > rubro.haber:
            cv.setFont('Helvetica', 12)
            cv.drawString(d, b, 'saldo deudor')
        else:
            if rubro.debe < rubro.haber:
                cv.setFont('Helvetica', 12)
                cv.drawString(d, b, 'saldo acreedor')
            else:
                cv.setFont('Helvetica', 12)
                cv.drawString(d, b, 'saldo cero')
        b -= 25
    cv.setFont('Helvetica', 12)
    fecha =  time.strftime("%d/%m/%y")
    hora = time.strftime("%H:%M:%S")
    cv.drawString(30, 30, '{} {} {} {} {} {}'.format('reporte generado por ', request.user.username, 'el', fecha, ' a las ', hora))
    cv.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
