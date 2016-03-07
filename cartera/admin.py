from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
from .resources import *


class detalle_admin(admin.ModelAdmin):
    list_display = ('suscriptor', 'contrato', 'servicio',
        'iddepartamento', 'idmunicipio', 'idbarrio', 'servicio',
        'saldo_pend_factura', 'integrado', 'estado', 'user')
    list_filter = ('categoria', 'iddepartamento', 'idmunicipio', 'idbarrio',
        'estado_corte', 'integrado', 'estado', 'user')

    def action_integrar(self, request, queryset):
        msj = integrar_detalle(queryset)
        self.message_user(request, msj)
    action_integrar.short_description = \
    "integrar clientes de los registros selecionados"

    actions = [action_integrar]

admin.site.register(Detalle, detalle_admin)


class import_model_admin(ImportExportModelAdmin):
    list_display = ('suscriptor', 'contrato', 'servicio',
        'departamento', 'localidad', 'barr_contacto', 'servicio',
        'saldo_pend_factura')

    def action_integrar(self, request, queryset):
        for obj in queryset:
            obj.integrar()
    action_integrar.short_description = \
    "actualizar cartera mora y rebajas"

    actions = [action_integrar]

admin.site.register(import_model, import_model_admin)


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
    readonly_fields = ('code', 'name', 'identificacion', 'departamento',
        'municipio', 'barrio', 'zona', 'comentario', 'direccion')
    fieldsets = (
        ('Datos Generales', {
                'classes': ('grp-collapse grp-open', ),
                'fields': (
                            'name', ('code', 'identificacion'),
                            ('departamento', 'municipio', 'barrio'),
                            'zona', 'direccion', 'comentario'
                        )
        }),
        ("Detalle de Mora", {"classes":
            ("placeholder detalle_set-group",), "fields": ()}),
        ("Promesas de Pago", {"classes":
            ("placeholder promesapago_set-group",), "fields": ()}),
        ("Facturas en Distribucion", {"classes":
            ("placeholder entrega_set-group",), "fields": ()}),
        ('Ubicacion Exacta', {
                'classes': ('grp-collapse grp-closed', ),
                'fields': ('position', )
        }),
                            )
    inlines = [detalle_cartera, promesas_cliente, entregas_cliente]

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