from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
from .resources import *


class detalle_admin(admin.ModelAdmin):
    resource_class = ccorriente_resouce
    list_display = ('suscriptor', 'contrato', 'servicio',
        'iddepartamento',
        'idmunicipio', 'idbarrio', 'servicio',
        'saldo_pend_factura', 'integrado', 'estado', 'user')
    list_filter = ('categoria', 'iddepartamento', 'idmunicipio', 'idbarrio',
        'estado_corte', 'integrado', 'estado', 'user')

    def action_integrar(self, request, queryset):
        for d in queryset:
            d.integrar()
    action_integrar.short_description = \
    "integrar clientes de los registros selecionados"

    actions = [action_integrar]


admin.site.register(Detalle, detalle_admin)


class cartera_corriente_admin(ImportExportModelAdmin):
    resource_class = ccorriente_resouce

admin.site.register(Corriente, cartera_corriente_admin)


class rebaja_corriente_admin(ImportExportModelAdmin):
    resource_class = ccorriente_resouce

admin.site.register(Rebaja, rebaja_corriente_admin)


class mora_corriente_admin(ImportExportModelAdmin):
    resource_class = ccorriente_resouce

admin.site.register(Mora, mora_corriente_admin)


class base_tabular(admin.TabularInline):
    extra = 0
    classes = ('grp-collapse grp-open',)


class detalle_cartera(base_tabular):
    model = Detalle
    fields = ('factura', 'factura_interna', 'no_cupon', 'no_fiscal',
        'fecha_fact', 'fecha_venc', 'tipo_mora', 'saldo_pend_factura',
        'fecha_asignacion', 'comentario', 'pagado')
    readonly_fields = ('factura', 'factura_interna', 'no_cupon', 'no_fiscal',
        'fecha_fact', 'fecha_venc', 'tipo_mora', 'saldo_pend_factura',
        'fecha_asignacion', 'comentario', 'pagado')


class promesas_cliente(base_tabular):
    model = PromesaPago


class cortes_cliente(base_tabular):
    model = Corte


class entregas_cliente(base_tabular):
    model = Entrega


class cliente_admin(admin.ModelAdmin):
    list_display = ('code', 'name', 'identificacion', 'comentario',
        'position_ver')
    list_filter = ('departamento', 'municipio', 'position_ver')
    search_fields = ('code', 'name', 'identificacion', 'contrato')
    fields = ('code', 'name', 'identificacion', 'departamento', 'municipio',
        'barrio', 'zona', 'comentario', 'direccion', 'position')
    inlines = [detalle_cartera, promesas_cliente]

admin.site.register(Cliente, cliente_admin)


class cortes_admin(admin.ModelAdmin):
    list_display = ('numero', 'fecha_asignacion', 'departamento', 'municipio',
        'barrio')
    list_filter = ('departamento', 'municipio')
    search_fields = ('numero',)

admin.site.register(Corte, cortes_admin)


class tipo_gestion_admin(admin.ModelAdmin):
    list_display = ('signo', 'descripcion', 'resultado')


admin.site.register(TipoGestion, tipo_gestion_admin)


class promosion_admin(ImportExportModelAdmin):
    resource_class = promosion_resouce
    list_display = ('contrato', 'descuento', 'fecha_baja', 'fecha_vence',
        'integrado')
    actions = ['integrar']

    def integrar(self, request, queryset):
        for obj in queryset:
            obj.idcliente = obj.get_cliente()
    integrar.short_description = "integrar al sistema promosiones seleccionadas"

admin.site.register(Promosion, promosion_admin)


class tipo_mora_admin(admin.ModelAdmin):
    list_display = ('name', 'dias')


admin.site.register(TipoMora, tipo_mora_admin)