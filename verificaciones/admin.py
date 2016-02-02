from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
from .resources import *


class verificacion_admin(ImportExportModelAdmin):
    resource_class = verificacion_resouce
    list_display = ('id', 'contrato', 'solicitud', 'nombre_cliente', 'servicio',
        'categoria', 'departamento', 'municipio', 'barrio', 'direccion')
    list_filter = ('sucursal', 'departamento', 'servicio', 'categoria')


admin.site.register(Verificacion, verificacion_admin)
