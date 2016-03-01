from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *


class detalle_admin(ImportExportModelAdmin):
    #resource_class = detalle_resouce
    list_display = ('cliente', 'suscriptor', 'contrato', 'servicio',
        'departamento', 'localidad', 'barr_contacto', 'servicio',
        'saldo_pend_factura', 'integrado')
    list_filter = ('categoria', 'departamento', 'estado_corte', 'integrado')

    def action_integrar(self, request, queryset):
        for d in queryset:
            d.integrar()
    action_integrar.short_description = \
    "integrar clientes de los registros selecionados"

    actions = [action_integrar]


admin.site.register(Detalle, detalle_admin)


class detalle_cartera(admin.TabularInline):
    model = Detalle
    extra = 0
    fields = ('factura_interna', 'no_cupon', 'no_fiscal', 'fecha_fact',
        'fecha_venc', 'tipo_mora', 'saldo_pend_factura')


class cliente_admin(admin.ModelAdmin):
    list_display = ('code', 'name', 'identificacion')
    list_filter = ('departamento', 'municipio')
    search_fields = ('code', 'name', 'identificacion')
    inlines = [detalle_cartera]

admin.site.register(Cliente, cliente_admin)