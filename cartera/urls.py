# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('cartera.views',
    url(r'^telecobranza/$',
    telecobranza, name='telecobranza'),
    url(r'^grabar_gestion_telefonica/$', 'grabar_gestion_telefonica',
        name='grabar_gestion_telefonica'),
)

