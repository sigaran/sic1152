from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import empleadocreate, EmpleadoList, empleadoupdate, planilla_import,empleadodelete

urlpatterns = [
        url(r'^empleado_create/', login_required(empleadocreate), name='empleado_create'),
        url(r'^empleado_list/', login_required(EmpleadoList.as_view()), name='empleado_list'),
        url(r'^empleado_edit/(?P<pk>.+)/', login_required(empleadoupdate), name='empleado_edit'),
        url(r'^empleado_del/(?P<pk>.+)/', login_required(empleadodelete), name='empleado_del'),
        url(r'^planilla_import',login_required(planilla_import), name='planilla_import')
    ]
