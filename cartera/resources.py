# -*- coding: utf-8 -*-
from import_export import resources
from .models import *


class ccorriente_resouce(resources.ModelResource):
    class Meta:
        model = Corriente

        fields = ('id', 'contrato', 'departamento', 'localidad',
            'barr_contacto', 'servicio', 'factura', 'no_cupon',
            'saldo_pend_factura', 'ciclo', 'mes', 'ano', 'suscriptor',
            'direccion', 'tipo_cartera', 'comentario')

        export_order = ('id', 'contrato', 'departamento', 'localidad',
            'barr_contacto', 'servicio', 'factura', 'no_cupon',
            'saldo_pend_factura', 'ciclo', 'mes', 'ano', 'suscriptor',
            'direccion', 'tipo_cartera', 'comentario')


class cmora_resouce(resources.ModelResource):
    class Meta:
        model = Mora

        fields = ('id', 'cliente', 'producto', 'categoria', 'contrato', 'nit',
            'departamento', 'localidad', 'barr_contacto',
            'servicio', 'factura', 'no_fiscal',
            'ciclo', 'ano', 'mes', 'fecha_fact', 'fecha_venc', 'tipo_mora',
            'estado_corte', 'fecha_instalacion', 'descr_plan', 'tecnologia',
            'canal_venta', 'ejecutivo_venta',
            'tel_contacto', 'tel_instalacion', 'tel_contacto_cliente',
            'suscriptor', 'direccion', 'fecha_asignacion', 'comentario')

        export_order = ('id', 'cliente', 'producto', 'categoria', 'contrato',
            'nit', 'departamento', 'localidad', 'barr_contacto',
            'servicio', 'factura', 'no_fiscal',
            'ciclo', 'ano', 'mes', 'fecha_fact', 'fecha_venc', 'tipo_mora',
            'estado_corte', 'fecha_instalacion', 'descr_plan', 'tecnologia',
            'canal_venta', 'ejecutivo_venta',
            'tel_contacto', 'tel_instalacion', 'tel_contacto_cliente',
            'suscriptor', 'direccion', 'fecha_asignacion', 'comentario')


class crebaja_resouce(resources.ModelResource):
    class Meta:
        model = Rebaja

        fields = ('id', 'cliente', 'producto', 'categoria', 'contrato', 'nit',
            'departamento', 'localidad', 'barr_contacto',
            'servicio', 'factura', 'no_fiscal',
            'ciclo', 'ano', 'mes', 'fecha_fact', 'fecha_venc', 'tipo_mora',
            'estado_corte', 'fecha_instalacion', 'descr_plan', 'tecnologia',
            'canal_venta', 'ejecutivo_venta',
            'tel_contacto', 'tel_instalacion', 'tel_contacto_cliente',
            'suscriptor', 'direccion', 'fecha_asignacion', 'comentario')

        export_order = ('id', 'cliente', 'producto', 'categoria', 'contrato',
            'nit', 'departamento', 'localidad', 'barr_contacto',
            'servicio', 'factura', 'no_fiscal',
            'ciclo', 'ano', 'mes', 'fecha_fact', 'fecha_venc', 'tipo_mora',
            'estado_corte', 'fecha_instalacion', 'descr_plan', 'tecnologia',
            'canal_venta', 'ejecutivo_venta',
            'tel_contacto', 'tel_instalacion', 'tel_contacto_cliente',
            'suscriptor', 'direccion', 'fecha_asignacion', 'comentario')


class promosion_resouce(resources.ModelResource):
    class Meta:
        model = Promosion
        fields = ('contrato', 'descuento', 'fecha_baja', 'fecha_vence')