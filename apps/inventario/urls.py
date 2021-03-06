from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import entrada_create, materialist, salida_create, productolist, pentrada_create,psalida_create


urlpatterns = [
    url(r'^materia_create/', login_required(entrada_create), name='materia_create'),
    url(r'^materia_salida/', login_required(salida_create), name='materia_salida'),
    url(r'^materia_list/', login_required(materialist), name='materia_list'),
    url(r'^producto_create/', login_required(pentrada_create), name='producto_create'),
    url(r'^producto_salida/', login_required(psalida_create), name='producto_salida'),
    url(r'^producto_list/', login_required(productolist), name='producto_list'),
    ]