# -*- coding: utf-8 -*-
from import_export import resources
from .models import *


class paquete_resouce(resources.ModelResource):
    class Meta:
        model = Paquete
        fields = ('contrato', 'factura', 'ciclo', 'mes', 'ano', 'cliente',
                  'direccion', 'barrio', 'municipio', 'departamento',
                  'distribuidor', 'ruta', 'zona', 'segmento', 'tarifa',
                  'idbarrio', 'iddepartemento', 'idmunicipio', 'servicio',
                  'total_mes_factura',)
        #exclude = ('id',)
