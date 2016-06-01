
from django.conf.urls import *
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = patterns('home.views',
    url(r'^info_barrio/$', 'info_barrio', name='info_barrio'),
    url(r'^barrios_huerfanos/$',
        login_required(barrios_huerfanos.as_view(), login_url='/admin/login/'),
        name='barrios_huerfanos'),
    url(r'^reporte_gestiones/$',
        login_required(reporte_gestiones.as_view(), login_url='/admin/login/'),
        name='reporte_gestiones'),
    url(r'^panel_asignacion/$',
        login_required(panel_asignacion.as_view(), login_url='/admin/login/'),
        name='panel_asignacion'),
    url(r'^asignar_barrio/$', 'asignar_barrio', name='asignar_barrio'),
    url(r'^carga_informacion/$', carga_informacion.as_view(),
        name='carga_informacion'),
    url(r'^get_zonas/$', 'get_zonas', name='get_zonas'),
    url(r'^get_users_zona/$', 'get_users_zona', name='get_zonas'),
    url(r'^entregas_pendientes/$', 'entregas_pendientes',
        name='entregas_pendientes'),
    url(r'^cobros_pendientes/$', 'cobros_pendientes',
        name='cobros_pendientes'),
    url(r'^cortes_pendientes/$', 'cortes_pendientes',
        name='cortes_pendientes'),
    url(r'^verificaciones_pendientes/$', 'verificaciones_pendientes',
        name='verificaciones_pendientes'),
    url(r'^telecobranza/$', telecobranza.as_view(),
        name='telecobranza'),
)