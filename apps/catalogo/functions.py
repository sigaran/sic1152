from .models import Cuenta, SubCuenta,Tipo,Rubro


def update_cuentas_now():
    tipos = Tipo.objects.all()
    rubros = Rubro.objects.all()
    cuentas = Cuenta.objects.all()
    subcuentas = SubCuenta.objects.all()
    for tipo in tipos:
        for rubro in rubros:
            for cta in cuentas:
                cta.saldo = 0
                cta.debe = 0
                cta.haber = 0
                for sub_cta in subcuentas:
                    sub_cta.saldo = float(abs(sub_cta.debe - sub_cta.haber))
                    sub_cta.save()
                    if cta == sub_cta.padre:
                        cta.debe += float(sub_cta.debe)
                        cta.haber += float(sub_cta.haber)
                cta.saldo = float(abs(cta.debe - cta.haber))
                cta.save()
                if cta.rubro == rubro:
                    rubro.debe += float(cta.debe)
                    rubro.haber += float(cta.haber)
            rubro.saldo = float(abs(rubro.debe - rubro.haber))
            rubro.save()
            if rubro.tipo == tipo:
                tipo.debe += float(rubro.debe)
                tipo.haber += float(rubro.haber)
        tipo.saldo = float(abs(tipo.debe - tipo.haber))
        tipo.save()


def reset_subcuentas_now():
    subcuentas = SubCuenta.objects.all()
    for cta in subcuentas:
        cta.saldo = 0
        cta.debe = 0
        cta.haber = 0
    return subcuentas
