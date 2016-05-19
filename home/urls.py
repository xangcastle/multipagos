from django.conf.urls import *
from .views import *

urlpatterns = patterns('home.views',
    url(r'^info_barrio/$', 'info_barrio', name='info_barrio'),
    url(r'^barrios_huerfanos/$', barrios_huerfanos.as_view(),
        name='barrios_huerfanos'),
)