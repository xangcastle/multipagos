from django.contrib import admin
from django.contrib.admin import site
import adminactions.actions as actions
from import_export.admin import ImportExportModelAdmin
from .models import *
from .resources import *
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from .views import *
from digitalizacion.models import *
from django import forms
from django.core.context_processors import csrf
from digitalizacion.api import generar_paginas
from django.conf import settings
import os
from django.http.response import HttpResponse
from django.core.servers.basehttp import FileWrapper
actions.add_to_site(site)
from datetime import datetime
from .views import cargar_para_cobro
from daterange_filter.filter import DateRangeFilter
from django.contrib.admin import widgets
from django.http import HttpResponseRedirect


def download_file(path):
    if not os.path.exists(path):
        return HttpResponse('Sorry. This file is not available.')
    else:
        response = HttpResponse(FileWrapper(file(path)),
            content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=%s' % \
        os.path.basename(path)
        return response


class entidad_admin(ImportExportModelAdmin):
    list_display = ('code', 'name')
    #actions = ['activar', 'inactivar']
    ordering = ('code',)
    search_fields = ('code', 'name')
    ordering = ('name',)

    def inactivar(self, request, queryset):
        queryset.update(activo=False)
    inactivar.short_description = "Deactivate selected objects"

    def activar(self, request, queryset):
        queryset.update(activo=True)
    activar.short_description = "Activate selected objects"


class base_tabular(admin.TabularInline):
    classes = ('grp-collapse grp-open',)
    extra = 0


class paquete_admin(ImportExportModelAdmin):
    date_hierarchy = "fecha_entrega"
    #resource_class = paquete_resouce

    search_fields = ('factura', 'contrato', 'cliente', 'barra')

    list_display = ('factura', 'contrato', 'cliente', 'iddepartamento',
        'idmunicipio', 'idbarrio', 'estado', 'ciclo', 'mes', 'ano', 'user',
        'fecha_entrega', 'link_comprobante')

    list_filter = (('fecha_entrega', DateRangeFilter), 'iddepartamento',
        'idmunicipio', 'estado', 'ciclo', 'mes', 'ano', 'user', )

    #list_editable = ('comprobante',)
    fieldsets = (('Datos Generales', {
                'classes': ('grp-collapse grp-open',),
                'fields': (('factura', 'cliente', 'contrato'),
                            ('ciclo', 'mes', 'ano'),
                            ('iddepartamento', 'idmunicipio', 'barrio'),
                            ('direccion',),
                            ('telefono_contacto', 'ruta', 'zona'))}),
                ('Datos de Facturacion', {
                'classes': ('grp-collapse grp-open',),
                'fields': (('segmento', 'tarifa', 'servicio'),
                            ('cupon', 'total_mes_factura', 'valor_pagar'),
                            ('numero_fiscal', 'factura_interna', 'entrega'))}),
                ('Entrega y Digitalizacion', {
                'classes': ('grp-collapse grp-open',),
                'fields': (('comprobante', 'user'),
                            ('archivo', 'consecutivo', 'tipificacion'),
                            ('parentezco', 'recibe', 'fecha_entrega'),
                            'position', 'imagen')}))
    raw_id_fields = ('iddepartamento', 'idmunicipio')
    autocomplete_lookup_fields = {
        'fk': ['iddepartamento', 'idmunicipio'],
        }
    readonly_fields = ('factura', 'cliente', 'contrato', 'cupon', 'ciclo',
        'mes', 'ano', 'departamento', 'municipio', 'barrio', 'direccion',
        'telefono_contacto', 'ruta', 'zona', 'segmento', 'tarifa', 'servicio',
        'cupon', 'total_mes_factura', 'valor_pagar', 'numero_fiscal',
        'factura_interna', 'entrega', 'tipificacion',
        'archivo', 'consecutivo', 'parentezco', 'recibe',
        'fecha_entrega')
    actions = ['action_integrar', 'action_imprimir',
        'action_exportar', 'generar_pods']

    def action_integrar(self, request, queryset):
        msj = integrar(queryset)
        self.message_user(request, msj)
    action_integrar.short_description = 'integrar facturas seleccionadas'

    def action_exportar(self, request, queryset):
        exportar_media_temp(queryset)
        queryset.update(exportado=True)
    action_exportar.short_description = 'exportar pdf facturas seleccionadas'

    def action_imprimir(self, request, queryset):
        imprimir(queryset, request.user)
    action_imprimir.short_description = \
    'cargar impresion de los comprobantes seleccionadas'

    def generar_pods(self, request, queryset):

        numero = 1
        comprobantes = queryset.order_by('archivo', 'consecutivo')
        for p in comprobantes:
            p.orden_impresion = numero
            p.save()
            numero += 1
        paginas = generar_paginas(comprobantes)
        ctx = {'paginas': paginas}
        response = render_to_response('metropolitana/comprobante.html',
            ctx, context_instance=RequestContext(request))
        #response = PDFTemplateResponse(request=request,
                               #template='metropolitana/comprobante.html',
                               #filename="comprobantes.pdf",
                               #context=ctx,
                               #show_content_in_browser=False,
                               #)
        return response


class cliente_admin(entidad_admin):
    list_display = ('contrato', 'name', 'departamento', 'municipio', 'barrio',
        'direccion', 'telefono_contacto', 'valor_pagar')
    list_filter = ('departamento', 'municipio', 'barrio', 'segmento', 'tarifa',
        'servicio')


class estadistica_departamento(base_tabular):
    model = EstadisticaDepartamento
    fields = ('departamento', 'total', 'entregados', 'pendientes')
    readonly_fields = ('departamento', 'total', 'entregados', 'pendientes')


class estadistica_ciclo(admin.ModelAdmin):
    list_display = ('code', 'ano', 'mes', 'ciclo', 'total', 'entregados',
        'pendientes', 'rendidos', 'rendiciones', 'por_rendir',
        'cumplimiento', 'estado')
    list_filter = ('ano', 'mes')
    ordering = ['-ano', '-mes', 'ciclo']
    fieldsets = (
        ('Datos del Ciclo', {'classes': ('grp-collapse grp-open',),
            'fields': (('ano', 'mes', 'ciclo'),
                ('total', 'entregados', 'pendientes'))}),
                )
    readonly_fields = ('ano', 'ciclo', 'mes', 'total', 'entregados',
        'pendientes')
    actions = ['crear_rendicion', 'action_integrar', 'corregir_media',
        'generar_rendicion', 'generar_pods', 'generar_lista_distribucion',
        'cerrar_ciclo', 'action_cagar_cartera']
    inlines = [estadistica_departamento]
    list_per_page = 10

    def crear_rendicion(self, request, queryset):
        mensaje = ""
        for c in queryset:
            qs = c.crear_nueva_rendicion()
            if qs[0]:
                mensaje += \
                "\n rendicion %s creada, %s comprobantes incluidos en ella" \
                % (str(qs[0]), str(qs[1].count()))
            else:
                rs = ", ".join(str(r) for r in qs[1].order_by('entrega_numero'
                ).distinct('entrega_numero'
                ).values_list('entrega_numero', flat=True))
                mensaje += "rendiciones %s generadas del ciclo %s"  \
                % (rs, str(c.ciclo))
        self.message_user(request, mensaje)
    crear_rendicion.short_description = \
    'crear rendicion de ciclos seleccionados'

    class numero_rendicion(forms.Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        numero = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
            choices=((1, 1), (2, 2), (3, 3)))

    class option_cartera(forms.Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        fecha_factura = forms.DateField(widget=widgets.AdminDateWidget())
        fecha_vencimiento_factura = forms.DateField(
            widget=widgets.AdminDateWidget())
        fecha_asignacion_cartera = forms.DateField(
            widget=widgets.AdminDateWidget())
        fecha_vencimiento_cartera = forms.DateField(
            widget=widgets.AdminDateWidget())

    def generar_rendicion(self, request, queryset):
        message = ""
        form = None

        if 'apply' in request.POST:
            form = self.numero_rendicion(request.POST)
            if form.is_valid():
                message = "Genero las redicion con los numero seleccionados"
                numero = form.cleaned_data['numero']
                for c in queryset:
                    for n in numero:
                        nombre = c.generar_rendicion(n)
                        temp_path = os.path.join(settings.MEDIA_ROOT, 'TEMP')
                        archivo = os.path.join(temp_path, nombre + '.tar.gz')
                        if os.path.exists(archivo):
                            cm1 = "rm -rf %s" % archivo
                            os.system(cm1)
                        cmd = "cd %s && tar -czvf %s.tar.gz %s" % (temp_path,
                            nombre, nombre)
                        os.system(cmd)
                        return download_file(archivo)

        if not form:
            form = self.numero_rendicion(
                initial={
                    '_selected_action': request.POST.getlist(
                        admin.ACTION_CHECKBOX_NAME)})

        data = {'queryset': queryset, 'form': form,
            'header_tittle': 'Por Favor seleccione los numero de redicion a generar',
            'explanation':
                'Se generaran rendicion a los siguientes ciclos:',
                'action': 'generar_rendicion'}

        data.update(csrf(request))
        self.message_user(request, message)
        return render_to_response('metropolitana/numero_rendicion.html', data)

    generar_rendicion.short_description = \
    "Generar rendicion de los ciclos seleccionados"

    def action_cagar_cartera(self, request, queryset):
        message = ""
        form = None

        if 'apply' in request.POST:
            form = self.option_cartera(request.POST)
            if form.is_valid():
                for c in queryset:
                    cargar_para_cobro(c, form.cleaned_data['fecha_factura'],
                    form.cleaned_data['fecha_vencimiento_factura'],
                    form.cleaned_data['fecha_asignacion_cartera'],
                    form.cleaned_data['fecha_vencimiento_cartera'])
                message = "facturas de los ciclos seleccionados fueron"\
                + " cargados a la aplicacion de cartera y cobro"
                self.message_user(request, message)
                return HttpResponseRedirect(
                    "/admin/metropolitana/estadisticaciclo")

        if not form:
            form = self.option_cartera(
                initial={
                    '_selected_action': request.POST.getlist(
                        admin.ACTION_CHECKBOX_NAME)})
        data = {'queryset': queryset, 'form': form,
            'header_tittle': 'Por Favor complete todos los campos',
            'explanation':
                'Los siguientes ciclo se pasaran a la aplicacion de Cartera:',
                'action': 'action_cagar_cartera'}
        data.update(csrf(request))
        self.message_user(request, message)
        return render_to_response('metropolitana/numero_rendicion.html', data)

    action_cagar_cartera.short_description = \
    'cargar aplicacion de cartera'

    def action_integrar(self, request, queryset):
        message = ""
        for c in queryset:
            ps = Paquete.objects.filter(ciclo=c.ciclo, mes=c.mes, ano=c.ano)
            message = integrar(ps)
        self.message_user(request, message)
    action_integrar.short_description = \
    'integrar ciclos seleccionados'

    def corregir_media(self, request, queryset):
        for c in queryset:
            verificar_media(c.paquetes())
    corregir_media.short_description = \
    "corregir media de los ciclos seleccionados"

    def delete_model(self, request, object):
        ps = Paquete.objects.filter(id__in=object.paquetes(
            ).values_list('id', flat=True))
        ps.delete()

    def generar_pods(self, request, queryset):
        for object in queryset:
            numero = 1
            comprobantes = object.paquetes().order_by('archivo', 'consecutivo')
            for p in comprobantes:
                p.orden_impresion = numero
                p.save()
                numero += 1
            paginas = generar_paginas(comprobantes)
            ctx = {'paginas': paginas}
            response = render_to_response('metropolitana/comprobante.html',
                ctx, context_instance=RequestContext(request))
            return response

        class Media:
            js = ("/static/metropolitana/js/estadistica.js",)

    def generar_lista_distribucion(self, request, queryset):
        for object in queryset:
            comprobantes = object.paquetes()
            data = lista_distribucion(comprobantes)
            ctx = {'data': data}
            response = render_to_response(
                'metropolitana/lista_distribucion.html', ctx,
                context_instance=RequestContext(request))
            return response

    def cerrar_ciclo(self, request, queryset):
        for o in queryset:
            cierre, create = CicloCierre.objects.get_or_create(code=o.code)
            cierre.cerrado = True
            cierre.fecha_cierre = datetime.now()
            cierre.save()
            o.paquetes().update(cerrado=True)


class tipificacion_admin(ImportExportModelAdmin):
    list_display = ('causa', 'descripcion')


class barrio_admin(entidad_admin):
    list_display = ('code', 'name', 'municipio', 'departamento')
    list_filter = ('departamento', 'municipio', 'revizado')
    fieldsets = (('', {
                'classes': ('grp-collapse grp-open',),
                'fields': (('code', 'revizado'),
                            ('name', ), ('departamento', 'municipio'),
                            'relative_position')}),)
    readonly_fields = ('code', 'revizado', 'name', 'departamento', 'municipio')


class municipio_admin(entidad_admin):
    list_display = ('code', 'name', 'departamento')
    list_filter = ('departamento', )


class zona_barrio_admin(base_tabular):
    model = zona_barrio
    extra = 0
    raw_id_fields = ('barrio', )
    autocomplete_lookup_fields = {
        'fk': ['barrio', ],
        }
    sortable_field_name = 'orden'


class zona_admin(admin.ModelAdmin):
    list_display = ('code', 'name', 'departamento')
    list_filter = ('departamento', )
    search_fields = ('departamento__name',)
    inlines = [zona_barrio_admin]
    readonly_fields = ('code', )
    fields = (('code', 'name'), 'departamento')
    actions = ['action_autoasignar', ]

    def action_autoasignar(self, request, queryset):
        for q in queryset:
            q.autoasignar()


class up_admin(ImportExportModelAdmin):
    list_display = ('id', 'user', 'fecha_entrega')


admin.site.register(Paquete, paquete_admin)
admin.site.register(EstadisticaCiclo, estadistica_ciclo)
admin.site.register(Tipificacion, tipificacion_admin)
admin.site.register(Barrio, barrio_admin)
admin.site.register(Municipio, municipio_admin)
admin.site.register(Departamento, entidad_admin)
admin.site.register(Zona, zona_admin)
admin.site.register(uPaquete, up_admin)


class ReEnvioClaroAdmin(ImportExportModelAdmin):

    list_display = ('id', 'barra', 'fecha_asignacion', 'fecha_envio', 'get_estado', 'enviado', )

    list_filter = ('paquete__estado', 'enviado', )

    search_fields = ('barra', 'paquete__estado', 'enviado', )

    def get_estado(self, obj):
        return obj.paquete.estado
    get_estado.short_description = 'Estado'
    get_estado.admin_order_field = 'paquete__estado'

admin.site.register(ReEnvioClaro, ReEnvioClaroAdmin)