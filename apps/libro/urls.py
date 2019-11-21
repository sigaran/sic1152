from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import createpdoble, diariolist, venta_mixta, compra_mixta


urlpatterns = [
    url(r'^pdoble_create/', login_required(createpdoble), name='pdoble_create'),
    url(r'^venta_mixta/', login_required(venta_mixta), name='venta_mixta'),
    url(r'^compra_mixta/', login_required(compra_mixta), name='compra_mixta'),
    url(r'^diario_list/', login_required(diariolist), name='diario_list'),
    ]