from django.db import models
from django.core.validators import MinLengthValidator


class Empleado(models.Model):
    codigo = models.CharField(primary_key=True, max_length=9, validators=[MinLengthValidator(9)])
    nombres = models.CharField(max_length=40)
    puesto = models.CharField(max_length=40)
    fecha =models.DateField()
    salario = models.FloatField()
    isss = models.FloatField()
    renta = models.FloatField()
    afp = models.FloatField()
    desc = models.FloatField()

    sal_neto = models.FloatField()

    def __str__(self):
        return '{} {} {}'.format(self.codigo, self.nombres, self.puesto)

    class Meta:
        ordering = '-codigo',
