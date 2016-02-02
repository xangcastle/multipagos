from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *


class verificacion_admin(ImportExportModelAdmin):
    list_display = ('contrato', 'solicitud', 'nombre_cliente', 'servicio',
        'categoria', 'departamento', 'municipio', 'barrio', 'direccion')
    list_filter = ('sucursal', 'departamento', 'servicio', 'categoria')


admin.site.register(Verificacion, verificacion_admin)
