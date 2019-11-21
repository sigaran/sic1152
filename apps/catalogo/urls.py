from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import cuentalist, cuentacreate, subcuentacreate, Search_Ct, catalogo_report,cuentaupdate,subcuentaupdate


urlpatterns = [
    url(r'^cuentas_list/', login_required(cuentalist), name='cuenta_list'),
    url(r'^cuenta_create/(?P<pk>.+)/', login_required(cuentacreate), name='cuenta_create'),
    url(r'^cuenta_update/(?P<pk>.+)/', login_required(cuentaupdate), name='cuenta_update'),
    url(r'^subcuenta_update/(?P<pk>.+)/', login_required(subcuentaupdate), name='subcuenta_update'),
    url(r'^subcuenta_create/(?P<pk>.+)/', login_required(subcuentacreate), name='subcuenta_create'),
    url(r'^search_cat', Search_Ct.as_view(), name='search_cat'),
    url(r'^catalogo_report', catalogo_report, name='catalogo_report')
    ]