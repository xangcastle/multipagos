from django.conf.urls import *

urlpatterns = patterns('',
    url(r'^get_user/$', 'movil.views.get_user', name='get_user'),
    url(r'^get_paquetes/$', 'movil.views.get_paquetes', name='get_paquetes'),
    url(r'^get_paquete/$', 'movil.views.get_paquete', name='get_paquete'),
    url(r'^get_estadisticadepartamentos/$',
   'movil.views.estadisticasDepartamento',
   name='get_estadisticadepartamentos'),
    url(r'^get_departamentos/$', 'movil.views.get_departamentos',
        name='get_departamentos'),
    url(r'^get_estadisticas_by_user/$', 'movil.views.estadisticas_by_user',
        name='get_estadisticas_by_user'),
    url(r'^get_verificacion/$', 'movil.views.get_verificacion',
        name='get_verificacion'),
)

