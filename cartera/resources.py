# -*- coding: utf-8 -*-
from import_export import resources
from .models import *


class detalle_resouce(resources.ModelResource):
    class Meta:
        model = Detalle
        fields = ('cliente', 'producto', 'categoria', 'contrato', 'nit',
            'departamento', 'localidad', 'barr_contacto', 'cuenta_cobro',
            'servicio', 'factura_interna', 'no_cupon', 'no_fiscal',
            'ciclo', 'ano', 'mes', 'fecha_fact', 'fecha_venc', 'tipo_mora',
            'estado_corte', 'fecha_instalacion', 'descr_plan', 'tecnologia',
            'canal_venta', 'ejecutivo_venta', 'facturas_generadas',
            'tel_contacto', 'tel_instalacion', 'tel_contacto_cliente',
            'suscriptor', 'direccion', 'tipo_cartera', 'comentario')