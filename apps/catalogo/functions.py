from .models import SubCuenta,Tipo,Cuenta,Rubro


def update_cuentas_now():
    activo = Tipo.objects.get(codigo='1')
    pasivo = Tipo.objects.get(codigo='2')
    patrimonio = Tipo.objects.get(codigo='3')
    resultadod = Tipo.objects.get(codigo='4')
    resultado = Tipo.objects.get(codigo='5')

    activo.debe = 0
    activo.haber = 0
    activo.saldo = 0
    activo.save()

    pasivo.debe = 0
    pasivo.haber = 0
    pasivo.saldo = 0
    pasivo.save()

    patrimonio.saldo = 0
    patrimonio.debe = 0
    patrimonio.haber = 0
    patrimonio.save()

    resultadod.saldo = 0
    resultadod.debe = 0
    resultadod.haber = 0
    resultadod.save()

    resultado.debe = 0
    resultado.haber = 0
    resultado.saldo = 0
    resultado.save()

    rbosa = Rubro.objects.filter(tipo=activo)
    rbosp = Rubro.objects.filter(tipo=pasivo)
    rbosc = Rubro.objects.filter(tipo=patrimonio)
    rbosrd = Rubro.objects.filter(tipo=resultadod)
    rbosr = Rubro.objects.filter(tipo=resultado)

    ctasa = Cuenta.objects.filter(rubro__tipo__codigo='1')
    ctasp = Cuenta.objects.filter(rubro__tipo__codigo='2')
    ctasc = Cuenta.objects.filter(rubro__tipo__codigo='3')
    ctasrd = Cuenta.objects.filter(rubro__tipo__codigo='4')
    ctasr = Cuenta.objects.filter(rubro__tipo__codigo='5')
    for cta in ctasa:
        cta.debe = 0
        cta.haber = 0
        cta.saldo = 0
        cta.save()
    for ra in rbosa:
        ra.debe = 0
        ra.haber = 0
        ra.saldo = 0
        ra.save()
    for ctp in ctasp:
        ctp.debe = 0
        ctp.haber = 0
        ctp.saldo = 0
        ctp.save()
    for rp in rbosp:
        rp.debe = 0
        rp.haber = 0
        rp.saldo = 0
        ra.save()
    for ctc in ctasc:
        ctc.debe = 0
        ctc.haber = 0
        ctc.saldo = 0
        ctc.save()
    for rc in rbosc:
        rc.debe = 0
        rc.haber = 0
        rc.saldo = 0
        rc.save()
    for ctrd in ctasrd:
        ctrd.debe = 0
        ctrd.haber = 0
        ctrd.saldo = 0
        ctrd.save()
    for rd in rbosrd:
        rd.debe = 0
        rd.haber = 0
        rd.saldo = 0
        rd.save()
    for ctr in ctasr:
        ctr.debe = 0
        ctr.haber = 0
        ctr.saldo = 0
        ctr.save()
    for r in rbosr:
        r.debe = 0
        r.haber = 0
        r.saldo = 0
        r.save()

    subsa = SubCuenta.objects.filter(padre__rubro__tipo=activo)
    subsps = SubCuenta.objects.filter(padre__rubro__tipo=pasivo)
    subsc = SubCuenta.objects.filter(padre__rubro__tipo=patrimonio)
    subsrd = SubCuenta.objects.filter(padre__rubro__tipo=resultadod)
    subsr = SubCuenta.objects.filter(padre__rubro__tipo=resultado)

    for sca in subsa:
        sca.padre.debe += float(sca.debe)
        sca.padre.haber += float(sca.haber)
        sca.padre.saldo = float(abs(sca.padre.debe - sca.padre.haber))
        sca.padre.save()
        sca.padre.rubro.debe += float(sca.debe)
        sca.padre.rubro.haber += float(sca.haber)
        sca.padre.rubro.saldo = float(abs(sca.padre.rubro.debe - sca.padre.rubro.haber))
        sca.padre.rubro.save()
        sca.padre.rubro.tipo.debe += float(sca.debe)
        sca.padre.rubro.tipo.haber += float(sca.haber)
        sca.padre.rubro.tipo.saldo = float(abs(sca.padre.rubro.tipo.debe - sca.padre.rubro.tipo.haber))
        sca.padre.rubro.tipo.save()
    for scps in subsps:
        scps.padre.debe += float(scps.debe)
        scps.padre.haber += float(scps.haber)
        scps.padre.saldo = float(abs(scps.padre.debe - scps.padre.haber))
        scps.padre.save()
        scps.padre.rubro.debe += float(scps.debe)
        scps.padre.rubro.haber += float(scps.haber)
        scps.padre.rubro.saldo = float(abs(scps.padre.rubro.debe - scps.padre.rubro.haber))
        scps.padre.rubro.save()
        scps.padre.rubro.tipo.debe += float(scps.debe)
        scps.padre.rubro.tipo.haber += float(scps.haber)
        scps.padre.rubro.tipo.saldo = float(abs(scps.padre.rubro.tipo.debe - scps.padre.rubro.tipo.haber))
        scps.padre.rubro.tipo.save()
    for scc in subsc:
        scc.padre.debe += float(scc.debe)
        scc.padre.haber += float(scc.haber)
        scc.padre.saldo = float(abs(scc.debe - scc.haber))
        scc.padre.save()
        scc.padre.rubro.debe += float(scc.debe)
        scc.padre.rubro.haber += float(scc.haber)
        scc.padre.rubro.saldo = float(abs(scc.padre.rubro.debe - scc.padre.rubro.haber))
        scc.padre.rubro.save()
        scc.padre.rubro.tipo.debe += float(scc.debe)
        scc.padre.rubro.tipo.haber += float(scc.haber)
        scc.padre.rubro.tipo.saldo = float(abs(scc.padre.rubro.tipo.debe - scc.padre.rubro.tipo.haber))
        scc.padre.rubro.tipo.save()
    for srd in subsrd:
        srd.padre.debe += float(srd.debe)
        srd.padre.haber += float(srd.haber)
        srd.padre.saldo = float(abs(srd.debe - srd.haber))
        srd.padre.save()
        srd.padre.rubro.debe += float(srd.debe)
        srd.padre.rubro.haber += float(srd.haber)
        srd.padre.rubro.saldo = float(abs(srd.padre.rubro.debe - srd.padre.rubro.haber))
        srd.padre.rubro.save()
        srd.padre.rubro.tipo.debe += float(srd.debe)
        srd.padre.rubro.tipo.haber += float(srd.haber)
        srd.padre.rubro.tipo.saldo = float(abs(srd.padre.rubro.tipo.debe - srd.padre.rubro.tipo.haber))
        srd.padre.rubro.tipo.save()
    for sr in subsr:
        sr.padre.debe += float(sr.debe)
        sr.padre.haber += float(sr.haber)
        sr.padre.saldo = float(abs(sr.debe - sr.haber))
        sr.padre.save()
        sr.padre.rubro.debe += float(sr.debe)
        sr.padre.rubro.haber += float(sr.haber)
        sr.padre.rubro.saldo = float(abs(sr.padre.rubro.debe - sr.padre.rubro.haber))
        sr.padre.rubro.save()
        sr.padre.rubro.tipo.debe += float(sr.debe)
        sr.padre.rubro.tipo.haber += float(sr.haber)
        sr.padre.rubro.tipo.saldo = float(abs(sr.padre.rubro.tipo.debe - sr.padre.rubro.tipo.haber))
        sr.padre.rubro.tipo.save()


def reset_subcuentas_now():
    subcuentas = SubCuenta.objects.all()
    for cta in subcuentas:
        cta.saldo = 0
        cta.debe = 0
        cta.haber = 0
    return subcuentas
