# -*- coding: utf-8 -*-
from import_export import resources
from .models import *


class verificacion_resouce(resources.ModelResource):
    class Meta:
        model = Verificacion
        fields = ('id', 'fecha_alta', 'nombre_cliente', 'contrato', 'plan',
            'cedula', 'servicio', 'categoria', 'sucursal', 'vendedor',
            'departamento', 'municipio', 'barrio', 'direccion', 'telefono',
            'celular', 'costo_instalacion', 'equipo', 'serial', 'mac', 'sim',
            'solicitud')
