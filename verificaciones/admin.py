from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.template.context import RequestContext
from django.shortcuts import render_to_response,  get_object_or_404, render
from .models import *
from django.http import HttpResponseRedirect, HttpResponse
from .resources import *


class verificacion_admin(ImportExportModelAdmin):
    date_hierarchy = "fecha_entrega"

    resource_class = verificacion_resouce

    list_display = ('contrato', 'solicitud', 'nombre_cliente', 'servicio',
                    'categoria', 'iddepartamento', 'idmunicipio', 'idbarrio', 'direccion',
                    'fecha_entrega', 'user', 'estado')

    list_filter = ('sucursal', 'iddepartamento', 'idmunicipio',
                   'servicio', 'categoria', 'user', 'estado', 'integrado')

    fieldsets = (('Datos Generales', {
        'classes': ('grp-collapse grp-open',),
        'fields': (('contrato', 'solicitud', 'fecha_alta', 'fecha_instalacion'),
                   ('cedula', 'nombre_cliente', 'direccion'),
                   ('sucursal', 'plan', 'servicio'),
                   ('departamento', 'municipio', 'barrio'),
                   ('celular', 'telefono', 'costo_instalacion'),
                   ('equipo', 'serial', 'mac'),
                   ('sim', 'hasta_50', 'mas_50')
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

    readonly_fields = ('contrato', 'nombre_cliente', 'fecha_alta', 'fecha_instalacion',
                       'cedula', 'plan', 'servicio', 'sucursal', 'departamento', 'municipio',
                       'barrio', 'celular', 'direccion', 'telefono', 'costo_instalacion',
                       'equipo', 'serial', 'mac', 'sim', 'solicitud')

    search_fields = ('contrato', 'nombre_cliente', 'cedula', 'solicitud')

    actions = ['action_integrar', 'action_generar_instalacion_pdf']

    def action_integrar(self, request, queryset):
        msj = integrar(queryset)
        self.message_user(request, msj)
    action_integrar.short_description = 'integrar verificaciones seleccionadas'

    def action_generar_instalacion_pdf(self, request, queryset):
        '''
        return render(request, 'verificaciones/rpt_verificacion_dth.html', {
            'data': 'queryset',
        })
        '''
        print queryset.get().contrato
        ctx = {'data': queryset.get()}
        response = render_to_response(
            'verificaciones/rpt_verificacion_dth.html', ctx,
            context_instance=RequestContext(request))
        return response
        msj = 'Documento Generado Exitosamente!'
        self.message_user(request, msj)
    action_generar_instalacion_pdf.short_description = 'Generar Instalacion PDF'

admin.site.register(Verificacion, verificacion_admin)
