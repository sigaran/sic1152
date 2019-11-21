from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import empleadocreate, EmpleadoList, empleadoupdate, planilla_import

urlpatterns = [
        url(r'^empleado_create/', login_required(empleadocreate), name='empleado_create'),
        url(r'^empleado_list/', login_required(EmpleadoList.as_view()), name='empleado_list'),
        url(r'^empleado_edit/(?P<pk>.+)/', login_required(empleadoupdate), name='empleado_edit'),
        url(r'^planilla_import',login_required(planilla_import), name='planilla_import')
    ]
