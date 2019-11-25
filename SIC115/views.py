from django.contrib import messages
from django.shortcuts import render, redirect
from apps.catalogo.models import Tipo, Rubro
from apps.libro.models import Transaccion
from apps.catalogo.models import SubCuenta,Cuenta
from apps.catalogo.functions import update_cuentas_now
from .forms import RegisterForm
from apps.catalogo.functions import reset_subcuentas_now
import time
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse


def diario_report(request):

    if request.POST:
        try:
            f_i = request.POST['inicio']
            f_f = request.POST['fin']
            query = Transaccion.objects.filter(fecha__range=(f_i,f_f))
        except:
            messages.error(request,'fechas con formato incorrecto')
            return redirect('report_index')
        if query:
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=libro_diario.pdf'
            buffer = BytesIO()
            cv = canvas.Canvas(buffer, pagesize=A4)
            cv.setFont('Helvetica-Bold', 12)
            cv.drawString(220, 750, 'EMPRESA RECITEC')
            cv.drawString(150, 735, 'registro de transacciones del {} al {}'.format(f_i, f_f))
            a=30
            b=700
            c=260
            d=460
            conteo =0
            for T in query:
                if conteo == 44:
                    cv.showPage()
                    conteo = 0
                    cv.setFont('Helvetica-Bold', 12)
                    cv.drawString(30, 710, 'fecha')
                    cv.drawString(120, 710, 'descripcion')
                    cv.drawString(450, 710, 'monto')
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
    update_cuentas_now()
    ultimos = Transaccion.objects.all().order_by('-fecha')[:3][::-1]
    tipos = Tipo.objects.all()
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
    ultimos = Transaccion.objects.all().order_by('-fecha')[:3][::-1]
    return render(request, 'reportes.html',{'fecha':fecha,'ultimos':ultimos})


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


def bc_report(request):
    try:
        f_i = request.POST['inicio']
        f_f = request.POST['fin']
        filtroF = Transaccion.objects.filter(fecha__range=(f_i, f_f))
        filtroI = Transaccion.objects.filter(fecha__lt=f_i)
    except:
        messages.error(request, 'fechas con formato incorrecto')
        return redirect('report_index')
    if request.POST:
        filtroI = Transaccion.objects.filter(fecha__lt=f_i)  # <--- filtra el valor previo
        ctas = reset_subcuentas_now()
        if filtroI:
            for T in filtroI:
                for ct in ctas:
                    if T.tipo_transaccion == 0:
                        if ct == T.cargo:
                            ct.debe += float(T.monto)
                        else:
                            if ct == T.abono:
                                ct.haber += float(T.monto)
                    else:
                        if T.tipo_transaccion == 1:
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
                                else:
                                    if ct == T.abono_alt:
                                        ct.haber += float(T.monto_credito)
                    ct.saldo = float(abs(ct.debe - ct.haber))
            for T in filtroF:
                for ct in ctas:
                    if T.tipo_transaccion == 0:
                        if ct == T.cargo:
                            ct.debe += float(T.monto)
                        else:
                            if ct == T.abono:
                                ct.haber += float(T.monto)
                    else:
                        if T.tipo_transaccion == 1:
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
                                else:
                                    if ct == T.abono_alt:
                                        ct.haber += float(T.monto_credito)
                    ct.saldo = float(abs(ct.debe - ct.haber))
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=balance_comprobacion_{}_{}.pdf'.format(f_i, f_f)
            buffer = BytesIO()
            cv = canvas.Canvas(buffer, pagesize=A4)
            # encabezados
            cv.setFont('Helvetica-Bold', 12)
            cv.drawString(220, 750, 'EMPRESA RECITEC')
            cv.drawString(150, 735, 'balance de comprobacion del {} al {}'.format(f_i, f_f))
            a = 30
            b = 715
            c = 360
            d = 460
            conteo = 0
            t_debe = 0
            t_haber = 0.00
            cv.line(a, b, 550, b, )
            b -= 15
            cv.setFillColorRGB(0.92578125, 0.92578125, 0.92578125)
            cv.setStrokeColorRGB(0.92578125, 0.92578125, 0.92578125)
            cv.setFont('Helvetica-Bold', 42)
            cv.line(130, 443, 450, 443, )
            cv.line(130, 442, 450, 442, )
            cv.drawString(130, 400, 'CONFIDENCIAL')
            cv.line(130, 390, 450, 390, )
            cv.line(130, 389, 450, 389, )

            cv.setFillColorRGB(0, 0, 0)
            for ct in ctas:
                if conteo == 44:
                    cv.showPage()
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
                    b = 715
                cv.setFont('Helvetica', 12)
                if ct.saldo > 0:
                    if ct.debe > ct.haber:
                        cv.drawString(a, b, ct.nombre)
                        cv.drawString(c, b, ct.saldo.__str__())
                        b -= 25
                        t_debe += ct.saldo
                    else:
                        cv.drawString(a, b, ct.nombre)
                        cv.drawString(d, b, ct.saldo.__str__())
                        b -= 25
                        t_haber += ct.saldo
                conteo += 1
            cv.setFillColorRGB(0, 0, 0)
            cv.setStrokeColorRGB(0, 0, 0)
            cv.line(a, b, 550, b, )
            b -= 15
            cv.drawString(a, b, 'totales')
            cv.drawString(c, b, t_debe.__str__())
            cv.drawString(d, b, t_haber.__str__())
            cv.setFont('Helvetica', 12)
            fecha = time.strftime("%d/%m/%y")
            hora = time.strftime("%H:%M:%S")
            cv.drawString(30, 30,
                          '{} {} {} {} {} {}'.format('balance de comprobacion generado por ', request.user.username,
                                                     'el',
                                                     fecha, ' a las ', hora))
            cv.save()
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            return response
        else:
            if filtroF:
                for T in filtroF:
                    for ct in ctas:
                        if T.tipo_transaccion == 0:
                            if ct == T.cargo:
                                ct.debe += float(T.monto)
                            else:
                                if ct == T.abono:
                                    ct.haber += float(T.monto)
                        else:
                            if T.tipo_transaccion == 1:
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
                                    else:
                                        if ct == T.abono_alt:
                                            ct.haber += float(T.monto_credito)
                        ct.saldo = float(abs(ct.debe - ct.haber))
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=balance_comprobacion_{}_{}.pdf'.format(f_i,f_f)
                buffer = BytesIO()
                cv = canvas.Canvas(buffer, pagesize=A4)
                #encabezados
                cv.setFont('Helvetica-Bold', 12)
                cv.drawString(220, 750, 'EMPRESA RECITEC')
                cv.drawString(150, 735, 'balance de comprobacion del {} al {}'.format(f_i, f_f))
                a = 30
                b = 715
                c = 360
                d = 460
                conteo = 0
                t_debe = 0
                t_haber = 0.00
                cv.line(a,b,550, b, )
                b -=15
                cv.setFillColorRGB(0.92578125, 0.92578125, 0.92578125)
                cv.setStrokeColorRGB(0.92578125, 0.92578125, 0.92578125)
                cv.setFont('Helvetica-Bold', 42)
                cv.line(130, 443, 450, 443, )
                cv.line(130, 442, 450, 442, )
                cv.drawString(130, 400, 'CONFIDENCIAL')
                cv.line(130, 390, 450, 390, )
                cv.line(130, 389, 450, 389, )

                cv.setFillColorRGB(0, 0, 0)
                for ct in ctas:
                    if conteo == 44:
                        cv.showPage()
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
                        b = 715
                    cv.setFont('Helvetica',12)
                    if ct.saldo>0:
                        if ct.debe>ct.haber:
                            cv.drawString(a,b,ct.nombre)
                            cv.drawString(c,b,ct.saldo.__str__())
                            b -= 25
                            t_debe += ct.saldo
                        else:
                            cv.drawString(a,b,ct.nombre)
                            cv.drawString(d,b,ct.saldo.__str__())
                            b -= 25
                            t_haber += ct.saldo
                    conteo +=1
                cv.setFillColorRGB(0, 0, 0)
                cv.setStrokeColorRGB(0, 0, 0)
                cv.line(a, b, 550, b, )
                b -= 15
                cv.drawString(a,b,'totales')
                cv.drawString(c,b,t_debe.__str__())
                cv.drawString(d,b,t_haber.__str__())
                cv.setFont('Helvetica', 12)
                fecha = time.strftime("%d/%m/%y")
                hora = time.strftime("%H:%M:%S")
                cv.drawString(30, 30,
                              '{} {} {} {} {} {}'.format('balance de comprobacion generado por ', request.user.username, 'el',
                                                         fecha,' a las ', hora))
                cv.save()
                pdf = buffer.getvalue()
                buffer.close()
                response.write(pdf)
                return response
            else:
                messages.error(request, 'lo sentimos pero no existen transaciones para el periodo ingresado')
                return redirect('report_index')


def er_report(request):
    try:
        f_i = request.POST['inicio']
        f_f = request.POST['fin']
        filtroF = Transaccion.objects.filter(fecha__range=(f_i, f_f))
        filtroI = Transaccion.objects.filter(fecha__lt=f_i)
    except:
        messages.error(request, 'fechas con formato incorrecto')
        return redirect('report_index')
    if request.POST:
        filtroI = Transaccion.objects.filter(fecha__lt=f_i)  # <--- filtra el valor previo
        ctas = reset_subcuentas_now()
        if filtroI:
            if filtroF:
                utilidades = SubCuenta.objects.get(codigo='320101')
                for T in filtroI:
                    for ct in ctas:
                        if T.tipo_transaccion == 0:
                            if ct == T.cargo:
                                ct.debe += float(T.monto)
                            else:
                                if ct == T.abono:
                                    ct.haber += float(T.monto)
                        else:
                            if T.tipo_transaccion == 1:
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
                                    else:
                                        if ct == T.abono_alt:
                                            ct.haber += float(T.monto_credito)
                        ct.saldo = float(abs(ct.debe - ct.haber))
                for T in filtroF:
                    for ct in ctas:
                        if T.tipo_transaccion == 0:
                            if ct == T.cargo:
                                ct.debe += float(T.monto)
                            else:
                                if ct == T.abono:
                                    ct.haber += float(T.monto)
                        else:
                            if T.tipo_transaccion == 1:
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
                                    else:
                                        if ct == T.abono_alt:
                                            ct.haber += float(T.monto_credito)
                        ct.saldo = float(abs(ct.debe - ct.haber))
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=estado_resultado_{}_{}.pdf'.format(f_i, f_f)
                buffer = BytesIO()
                cv = canvas.Canvas(buffer, pagesize=A4)
                # encabezados
                cv.setFont('Helvetica-Bold', 12)
                cv.drawString(220, 750, 'EMPRESA RECITEC')
                cv.drawString(150, 735, 'estado de resultado del {} al {}'.format(f_i, f_f))
                cv.drawString(30,715,'cuenta')
                cv.drawString(360,715,'costos')
                cv.drawString(460,715,'ingresos')
                a = 30
                b = 700
                c = 360
                d = 460
                conteo = 0
                t_debe = 0.00
                t_haber = 0.00
                cv.line(a, b, 550, b, )
                b -= 15
                cv.setFillColorRGB(0.92578125, 0.92578125, 0.92578125)
                cv.setStrokeColorRGB(0.92578125, 0.92578125, 0.92578125)
                cv.setFont('Helvetica-Bold', 42)
                cv.line(130, 443, 450, 443, )
                cv.line(130, 442, 450, 442, )
                cv.drawString(130, 400, 'CONFIDENCIAL')
                cv.line(130, 390, 450, 390, )
                cv.line(130, 389, 450, 389, )

                cv.setFillColorRGB(0, 0, 0)
                for ct in ctas:
                    if conteo == 44:
                        cv.showPage()
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
                        b = 715
                    cv.setFont('Helvetica', 12)
                    if ct.padre.codigo == '5101' or ct.padre.codigo == '5102':
                        cv.drawString(a, b, ct.nombre)
                        cv.drawString(d, b, ct.saldo.__str__())
                        b -= 25
                        t_haber += ct.saldo
                    else:
                        if ct.padre.rubro.codigo == '41':
                            cv.drawString(a, b, ct.nombre)
                            cv.drawString(c, b, ct.saldo.__str__())
                            b -= 25
                            t_debe += ct.saldo
                    conteo += 1
                cv.setFillColorRGB(0, 0, 0)
                cv.setStrokeColorRGB(0, 0, 0)
                cv.line(a, b, 550, b, )
                b -= 15
                cv.drawString(a,b,'totales')
                cv.drawString(c,b,t_debe.__str__())
                cv.drawString(d,b,t_haber.__str__())
                b -= 15
                cv.drawString(a, b, 'utilidades')
                utilidades.haber = float(abs(t_debe - t_haber))
                utilidades.saldo = utilidades.haber
                utilidades.save()
                cv.drawString(d, b, utilidades.saldo.__str__())
                cv.setFont('Helvetica', 12)
                fecha = time.strftime("%d/%m/%y")
                hora = time.strftime("%H:%M:%S")
                cv.drawString(30, 30,
                              '{} {} {} {} {} {}'.format('estado de resultado generado por ', request.user.username,
                                                         'el',
                                                         fecha, ' a las ', hora))
                cv.save()
                pdf = buffer.getvalue()
                buffer.close()
                response.write(pdf)
                return response
            else:
                messages.error(request,'no existen transacciones para este periodo')
                return redirect('report_index')
        else:
            if filtroF:
                utilidades = SubCuenta.objects.get(codigo='320101')
                for T in filtroF:
                    for ct in ctas:
                        if T.tipo_transaccion == 0:
                            if ct == T.cargo:
                                ct.debe += float(T.monto)
                            else:
                                if ct == T.abono:
                                    ct.haber += float(T.monto)
                        else:
                            if T.tipo_transaccion == 1:
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
                                    else:
                                        if ct == T.abono_alt:
                                            ct.haber += float(T.monto_credito)
                        ct.saldo = float(abs(ct.debe - ct.haber))
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=estado:resultado_{}_{}.pdf'.format(f_i, f_f)
                buffer = BytesIO()
                cv = canvas.Canvas(buffer, pagesize=A4)
                # encabezados
                cv.setFont('Helvetica-Bold', 12)
                cv.drawString(220, 750, 'EMPRESA RECITEC')
                cv.drawString(150, 735, 'estado de resultado del {} al {}'.format(f_i, f_f))
                cv.drawString(30, 715, 'cuenta')
                cv.drawString(360, 715, 'costos')
                cv.drawString(460, 715, 'ingresos')
                a = 30
                b = 700
                c = 360
                d = 460
                conteo = 0
                t_debe = 0.00
                t_haber = 0.00
                cv.line(a, b, 550, b, )
                b -= 15
                cv.setFillColorRGB(0.92578125, 0.92578125, 0.92578125)
                cv.setStrokeColorRGB(0.92578125, 0.92578125, 0.92578125)
                cv.setFont('Helvetica-Bold', 42)
                cv.line(130, 443, 450, 443, )
                cv.line(130, 442, 450, 442, )
                cv.drawString(130, 400, 'CONFIDENCIAL')
                cv.line(130, 390, 450, 390, )
                cv.line(130, 389, 450, 389, )

                cv.setFillColorRGB(0, 0, 0)
                for ct in ctas:
                    if conteo == 44:
                        cv.showPage()
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
                        b = 715
                    cv.setFont('Helvetica', 12)
                    if ct.padre.codigo == '5101' or ct.padre.codigo == '5102':
                        cv.drawString(a, b, ct.nombre)
                        cv.drawString(d, b, ct.saldo.__str__())
                        b -= 25
                        t_haber += ct.saldo
                    else:
                        if ct.padre.rubro.codigo == '41':
                            cv.drawString(a, b, ct.nombre)
                            cv.drawString(c, b, ct.saldo.__str__())
                            b -= 25
                            t_debe += ct.saldo
                    conteo += 1
                cv.setFillColorRGB(0, 0, 0)
                cv.setStrokeColorRGB(0, 0, 0)
                b -= 15
                cv.drawString(a, b, 'totales')
                cv.drawString(c, b, t_debe.__str__())
                cv.drawString(d, b, t_haber.__str__())
                b -= 15
                cv.line(a, b, 550, b, )
                b -= 15
                cv.drawString(a, b, 'utilidades')
                utilidades.haber = float(abs(t_debe - t_haber))
                utilidades.saldo = utilidades.haber
                utilidades.save()
                cv.drawString(d, b, utilidades.saldo.__str__())
                cv.setFont('Helvetica', 12)
                fecha = time.strftime("%d/%m/%y")
                hora = time.strftime("%H:%M:%S")
                cv.drawString(30, 30,
                              '{} {} {} {} {} {}'.format('estado de resultado generado por ', request.user.username,
                                                         'el',
                                                         fecha, ' a las ', hora))
                cv.save()
                pdf = buffer.getvalue()
                buffer.close()
                response.write(pdf)
                return response
            else:
                messages.error(request, 'lo sentimos pero no existen transaciones para el periodo ingresado')
                return redirect('report_index')


def bg_report(request):
    try:
        f_i = request.POST['inicio']
        f_f = request.POST['fin']
        filtroF = Transaccion.objects.filter(fecha__range=(f_i, f_f))
    except:
        messages.error(request, 'fechas con formato incorrecto')
        return redirect('report_index')
    if request.POST:
        filtroI = Transaccion.objects.filter(fecha__lt=f_i)  # <--- filtra el valor previo
        ctas = reset_subcuentas_now()
        if filtroI:
            for T in filtroI:
                for ct in ctas:
                    if T.tipo_transaccion == 0:
                        if ct == T.cargo:
                            ct.debe += float(T.monto)
                        else:
                            if ct == T.abono:
                                ct.haber += float(T.monto)
                    else:
                        if T.tipo_transaccion == 1:
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
                                else:
                                    if ct == T.abono_alt:
                                        ct.haber += float(T.monto_credito)
                    ct.saldo = float(abs(ct.debe - ct.haber))
            for T in filtroF:
                for ct in ctas:
                    if T.tipo_transaccion == 0:
                        if ct == T.cargo:
                            ct.debe += float(T.monto)
                        else:
                            if ct == T.abono:
                                ct.haber += float(T.monto)
                    else:
                        if T.tipo_transaccion == 1:
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
                                else:
                                    if ct == T.abono_alt:
                                        ct.haber += float(T.monto_credito)
                    ct.saldo = float(abs(ct.debe - ct.haber))
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=balance_general_{}_{}.pdf'.format(f_i, f_f)
            buffer = BytesIO()
            cv = canvas.Canvas(buffer, pagesize=A4)
            # encabezados
            cv.setFont('Helvetica-Bold', 12)
            cv.drawString(220, 750, 'EMPRESA RECITEC')
            cv.drawString(150, 735, 'balance general del {} al {}'.format(f_i, f_f))
            cv.drawString(30,715,'cuenta')
            cv.drawString(360, 715, 'activos')
            cv.drawString(460, 715, 'participaciones')
            a = 30
            b = 700
            c = 360
            d = 460
            conteo = 0
            t_debe = 0
            t_haber = 0.00
            cv.line(a, b, 550, b, )
            b -= 15
            cv.setFillColorRGB(0.92578125, 0.92578125, 0.92578125)
            cv.setStrokeColorRGB(0.92578125, 0.92578125, 0.92578125)
            cv.setFont('Helvetica-Bold', 42)
            cv.line(130, 443, 450, 443, )
            cv.line(130, 442, 450, 442, )
            cv.drawString(130, 400, 'CONFIDENCIAL')
            cv.line(130, 390, 450, 390, )
            cv.line(130, 389, 450, 389, )

            cv.setFillColorRGB(0, 0, 0)
            for ct in ctas:
                if conteo == 44:
                    cv.showPage()
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
                    b = 715
                cv.setFont('Helvetica', 12)
                if ct.saldo > 0:
                    if ct.padre.rubro.tipo.codigo == '1':
                        cv.drawString(a, b, ct.nombre)
                        cv.drawString(c, b, ct.saldo.__str__())
                        b -= 25
                        t_debe += ct.saldo
                    else:
                        if ct.padre.rubro.tipo.codigo == '2' or ct.padre.rubro.tipo.codigo == '3':
                            cv.drawString(a, b, ct.nombre)
                            cv.drawString(d, b, ct.saldo.__str__())
                            b -= 25
                            t_haber += ct.saldo
                conteo += 1
            cv.setFillColorRGB(0, 0, 0)
            cv.setStrokeColorRGB(0, 0, 0)
            cv.line(a, b, 550, b, )
            b -= 15
            cv.drawString(a, b, 'totales')
            cv.drawString(c, b, t_debe.__str__())
            cv.drawString(d, b, t_haber.__str__())
            cv.setFont('Helvetica', 12)
            fecha = time.strftime("%d/%m/%y")
            hora = time.strftime("%H:%M:%S")
            cv.drawString(30, 30,
                          '{} {} {} {} {} {}'.format('balance general generado por ', request.user.username,
                                                     'el',
                                                     fecha, ' a las ', hora))
            cv.save()
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            return response
        else:
            if filtroF:
                for T in filtroF:
                    for ct in ctas:
                        if T.tipo_transaccion == 0:
                            if ct == T.cargo:
                                ct.debe += float(T.monto)
                            else:
                                if ct == T.abono:
                                    ct.haber += float(T.monto)
                        else:
                            if T.tipo_transaccion == 1:
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
                                    else:
                                        if ct == T.abono_alt:
                                            ct.haber += float(T.monto_credito)
                        ct.saldo = float(abs(ct.debe - ct.haber))
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=balance_general_{}_{}.pdf'.format(f_i,f_f)
                buffer = BytesIO()
                cv = canvas.Canvas(buffer, pagesize=A4)
                #encabezados
                cv.setFont('Helvetica-Bold', 12)
                cv.drawString(220, 750, 'EMPRESA RECITEC')
                cv.drawString(150, 735, 'balance general del {} al {}'.format(f_i, f_f))
                cv.drawString(30, 715, 'cuenta')
                cv.drawString(360, 715, 'activos')
                cv.drawString(460, 715, 'participaciones')
                a = 30
                b = 700
                c = 360
                d = 460
                conteo = 0
                t_debe = 0
                t_haber = 0.00
                cv.line(a,b,550, b, )
                b -=15
                cv.setFillColorRGB(0.92578125, 0.92578125, 0.92578125)
                cv.setStrokeColorRGB(0.92578125, 0.92578125, 0.92578125)
                cv.setFont('Helvetica-Bold', 42)
                cv.line(130, 443, 450, 443, )
                cv.line(130, 442, 450, 442, )
                cv.drawString(130, 400, 'CONFIDENCIAL')
                cv.line(130, 390, 450, 390, )
                cv.line(130, 389, 450, 389, )

                cv.setFillColorRGB(0, 0, 0)
                for ct in ctas:
                    if conteo == 44:
                        cv.showPage()
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
                        b = 715
                    cv.setFont('Helvetica',12)
                    if ct.saldo > 0:
                        if ct.padre.rubro.tipo.codigo == '1':
                            cv.drawString(a, b, ct.nombre)
                            cv.drawString(c, b, ct.saldo.__str__())
                            b -= 25
                            t_debe += ct.saldo
                        else:
                            if ct.padre.rubro.tipo.codigo == '2' or ct.padre.rubro.tipo.codigo == '3':
                                cv.drawString(a, b, ct.nombre)
                                cv.drawString(d, b, ct.saldo.__str__())
                                b -= 25
                                t_haber += ct.saldo
                    conteo +=1
                utilidades = SubCuenta.objects.get(codigo='320101')
                t_haber += utilidades.haber
                cv.drawString(a, b, utilidades.nombre)
                cv.drawString(d, b, utilidades.saldo.__str__())
                b -= 25
                cv.setFillColorRGB(0, 0, 0)
                cv.setStrokeColorRGB(0, 0, 0)
                cv.line(a, b, 550, b, )
                b -= 15
                cv.drawString(a,b,'totales')
                cv.drawString(c,b,t_debe.__str__())
                cv.drawString(d,b,t_haber.__str__())
                cv.setFont('Helvetica', 12)
                fecha = time.strftime("%d/%m/%y")
                hora = time.strftime("%H:%M:%S")
                cv.drawString(30, 30,
                              '{} {} {} {} {} {}'.format('balance general generado por ', request.user.username, 'el',
                                                         fecha,' a las ', hora))
                cv.save()
                pdf = buffer.getvalue()
                buffer.close()
                response.write(pdf)
                return response
            else:
                messages.error(request, 'lo sentimos pero no existen transaciones para el periodo ingresado')
                return redirect('report_index')
