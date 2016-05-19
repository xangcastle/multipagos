from django.conf.urls import *
from .views import *

urlpatterns = patterns('home.views',
    url(r'^info_barrio/$', 'info_barrio', name='info_barrio'),
    url(r'^barrios_huerfanos/$', barrios_huerfanos.as_view(),
        name='barrios_huerfanos'),
    url(r'^reporte_gestiones/$', reporte_gestiones.as_view(),
        name='reporte_gestiones'),
    url(r'^panel_asignacion/$', panel_asignacion.as_view(),
        name='panel_asignacion'),
    url(r'^asignar_barrio/$', 'asignar_barrio', name='asignar_barrio'),
)