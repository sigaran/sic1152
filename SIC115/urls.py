"""SIC115 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.conf.urls import url, include
from .views import index, usercreate, error_404, tipos_repot, rubros_repot, support, report_index,diario_report

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^register/', login_required(usercreate), name='register'),
    url(r'^home', index, name='index'),
    url(r'^support/', login_required(support), name='support'),
    url(r'^diario_report/', login_required(diario_report), name='diario_report'),
    url(r'^reports/', login_required(report_index), name='report_index'),
    url(r'^planilla/', include('apps.planilla.urls')),
    url(r'^catalogo/', include('apps.catalogo.urls')),
    url(r'^libro/', include('apps.libro.urls')),
    url(r'^inventario/', include('apps.inventario.urls')),
    url(r'tipos_report/', login_required(tipos_repot), name='tipos_report'),
    url(r'rubros_report/', login_required(rubros_repot), name='rubros_report'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^error_404/', login_required(error_404), name='404'),
    url(r'^', RedirectView.as_view(url='/home')),

]
