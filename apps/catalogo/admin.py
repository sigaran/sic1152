from django.contrib import admin
from .models import Cuenta, Rubro, Tipo, SubCuenta


admin.site.register(Cuenta)
admin.site.register(Rubro)
admin.site.register(Tipo)
admin.site.register(SubCuenta)

