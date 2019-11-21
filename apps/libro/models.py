from django.db import models
from apps.catalogo.models import Tipo, Rubro, Cuenta, SubCuenta
from django.utils import timezone


class Transaccion(models.Model):

    fecha = models.DateField(default=timezone.now, blank=True,)
    descripcion = models.CharField(max_length=50)
    cargo = models.ForeignKey(SubCuenta, on_delete=models.PROTECT, related_name="cargo")
    monto_contado = models.FloatField(default=0.00)
    monto_credito = models.FloatField(default=0.00)
    tipo_transaccion = models.IntegerField(default=0)
    cargo_alt = models.ForeignKey(SubCuenta, on_delete=models.PROTECT, related_name="cargo_alt", null=True, blank=True)
    descripcion_cargo = models.CharField(max_length=50)
    abono = models.ForeignKey(SubCuenta, on_delete=models.PROTECT, related_name="abono")
    abono_alt = models.ForeignKey(SubCuenta, related_name="abono_alt", on_delete=models.PROTECT, null=True, blank=True)
    descripcion_abono = models.CharField(max_length=50)
    monto = models.FloatField(default=0.00)

    def __str__(self):
        return '{} {}'.format(self.id, self.fecha)

