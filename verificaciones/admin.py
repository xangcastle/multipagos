from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
from .resources import *


class verificacion_admin(ImportExportModelAdmin):
    date_hierarchy = "fecha_entrega"
    resource_class = verificacion_resouce
    list_display = ('contrato', 'solicitud', 'nombre_cliente', 'servicio',
        'categoria', 'iddepartamento', 'idmunicipio', 'idbarrio', 'direccion',
        'fecha_entrega', 'user', 'estado')
    list_filter = ('sucursal', 'iddepartamento', 'idmunicipio', 'idbarrio',
        'servicio', 'categoria', 'user', 'estado', 'integrado')

    fieldsets = (('Datos Generales', {
                'classes': ('grp-collapse grp-open',),
                'fields': (('contrato', 'nombre_cliente', 'fecha_alta'),
                            ('cedula', 'plan', 'servicio'),
                            ('sucursal', 'departamento', 'municipio'),
                            ('barrio', 'celular'), 'direccion',
                            ('telefono', 'costo_instalacion'),
                            ('equipo', 'serial', 'mac'),
                            ('sim', 'solicitud')
                            )}),
                ('Verificacion de datos del Cliente', {
                'classes': ('grp-collapse grp-open',),
                'fields': (('direccion_corr',), 'direccion_ver',
                            ('tipo_vivienda', 'reside'),
                            ('telefono_ver', 'telefono_corr'),
                            ('celular_ver', 'celular_corr'),
                            ('telefono_trabajo',), 'position'
                            )}),
                ('Verificacion de datos del Servicio', {
                'classes': ('grp-collapse grp-open',),
                'fields': (('servicio_contratado', 'pago_instalacion',
                                'costo_instalacion_corr'),
                            ('conoce_tarifa', 'copia_contratos',
                                'satisfecho_servicio'),
                            ('producto_malo', 'mala_atencion',
                                'sin_promosiones'), 'otros',
                            ('equipo_corr', 'serial_corr', 'mac_corr'),
                            ('sim_corr', 'estado_equipos', 'visita_supervisor'),
                            'comentarios'
                            )}))

    readonly_fields = ('contrato', 'nombre_cliente', 'fecha_alta',
        'cedula', 'plan', 'servicio', 'sucursal', 'departamento', 'municipio',
        'barrio', 'celular', 'direccion', 'telefono', 'costo_instalacion',
        'equipo', 'serial', 'mac', 'sim', 'solicitud')
    search_fields = ('contrato', 'nombre_cliente', 'cedula', 'solicitud')
    actions = ['action_integrar']

    def action_integrar(self, request, queryset):
        msj = integrar(queryset)
        self.message_user(request, msj)
    action_integrar.short_description = 'integrar verificaciones seleccionadas'


admin.site.register(Verificacion, verificacion_admin)
