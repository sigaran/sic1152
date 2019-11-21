from django.db import models
from django.core.validators import MinLengthValidator


class Tipo(models.Model):
    nombre = models.CharField(max_length=35)
    codigo = models.CharField(primary_key=True, max_length=1, validators=[MinLengthValidator(1)])
    debe = models.FloatField(default=0.00)
    haber = models.FloatField(default=0.00)
    saldo = models.FloatField(default=0.00)

    class Meta:
        ordering = 'codigo',

    def __str__(self):
        return '{}'.format(self.nombre)


class Rubro(models.Model):
    nombre = models.CharField(max_length=35)
    codigo= models.CharField(primary_key=True, max_length=2, validators=[MinLengthValidator(2)])
    tipo = models.ForeignKey(Tipo, on_delete=models.PROTECT)
    debe = models.FloatField(default=0.00)
    haber = models.FloatField(default=0.00)
    saldo = models.FloatField(default=0.00)

    class Meta:
        ordering = 'codigo',

    def __str__(self):
        return '{} {}'.format(self.codigo, self.nombre)


class Cuenta(models.Model):
    nombre = models.CharField(max_length=35)
    codigo = models.CharField(primary_key=True,  blank=True, max_length=4, validators=[MinLengthValidator(4)])
    rubro = models.ForeignKey(Rubro, blank=True, on_delete=models.PROTECT)
    debe = models.FloatField(default=0.00)
    haber = models.FloatField(default=0.00)
    saldo = models.FloatField(default=0.00)

    class Meta:
        ordering = 'codigo',

    def __str__(self):
        return '{} {}'.format(self.codigo, self.nombre)


class SubCuenta(models.Model):
    nombre = models.CharField(max_length=35)
    codigo = models.CharField(primary_key=True, blank=True, max_length=6, validators=[MinLengthValidator(6)])
    padre = models.ForeignKey(Cuenta, blank=True, on_delete=models.PROTECT)
    debe = models.FloatField(default=0.00)
    haber = models.FloatField(default=0.00)
    saldo = models.FloatField(default=0.00)

    class Meta:
        ordering = 'codigo',

    def __str__(self):
        return '{} {}'.format(self.codigo, self.nombre)
