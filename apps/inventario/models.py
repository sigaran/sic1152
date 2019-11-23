from django.db import models
from django.utils import timezone


class Materia(models.Model):
    tipo = models.IntegerField(default=0)
    fecha = models.DateField(default=timezone.now, blank=True)
    cantidad = models.IntegerField()
    existencias = models.IntegerField()
    precio_unit = models.FloatField()
    monto = models.FloatField()

    class Meta:
        ordering = '-fecha',

    def __str__(self):
        return '{} '.format( self.fecha)


class Producto(models.Model):
    tipo = models.IntegerField(default=0)
    fecha = models.DateField(default=timezone.now, blank=True)
    cantidad = models.IntegerField()
    existencias = models.IntegerField()
    precio_unit = models.FloatField()
    monto = models.FloatField()

    class Meta:
        ordering = '-fecha',

    def __str__(self):
        return '{} '.format( self.fecha)

