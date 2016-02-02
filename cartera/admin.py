from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
#from .resources import *


class detalle_admin(ImportExportModelAdmin):
    #resource_class = detalle_resouce
    list_display = ('cliente', 'suscriptor', 'contrato', 'servicio',
        'departamento', 'localidad', 'barr_contacto', 'servicio', 'saldo_pend')
    list_filter = ('categoria', 'departamento', 'estado_corte')


admin.site.register(Detalle, detalle_admin)
