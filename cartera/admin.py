from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
#from .resources import *


class mipropioadminclass(admin.ModelAdmin):

    def get_total_fiels(self):
        if self.total_fields:
            return self.total_fields


class detalle_admin(ImportExportModelAdmin):
    #resource_class = detalle_resouce
    list_display = ('cliente', 'suscriptor', 'contrato', 'servicio',
        'departamento', 'localidad', 'barr_contacto', 'servicio',
        'saldo_pend_factura')
    list_filter = ('categoria', 'departamento', 'estado_corte')

    def action_integrar(self, request, queryset):
        for d in queryset:
            d.intengrar()
    action_integrar.short_description = \
    "integrar clientes de los registros selecionados"

    actions = [action_integrar]


admin.site.register(Detalle, detalle_admin)


class cliente_admin(mipropioadminclass):
    list_display = ('code', 'name', 'identificacion')
    list_filter = ('departamento', 'municipio')
    search_fields = ('code', 'name', 'identificacion')

admin.site.register(Cliente, cliente_admin)