# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('digitalizacion.views',
    url(r'^carga_manual/(?P<id>.*)/$', 'carga_manual',
        name='carga_manual'),
    url(r'^autocomplete_pod/$', 'autocomplete_pod',
        name='autocomplete_pod'),
    url(r'^cargar_pod/$', 'cargar_pod',
        name='cargar_pod'),
)
