# -*- coding: utf-8 -*-
from import_export import resources
from .models import *


class ccorriente_resouce(resources.ModelResource):
    class Meta:
        model = import_model

        fields = ('id', 'contrato', 'departamento', 'localidad',
            'barr_contacto', 'servicio', 'factura', 'no_cupon',
            'saldo_pend_factura', 'ciclo', 'mes', 'ano', 'suscriptor',
            'direccion', 'tipo_cartera', 'comentario')

        export_order = ('id', 'contrato', 'departamento', 'localidad',
            'barr_contacto', 'servicio', 'factura', 'no_cupon',
            'saldo_pend_factura', 'ciclo', 'mes', 'ano', 'suscriptor',
            'direccion', 'tipo_cartera', 'comentario')
