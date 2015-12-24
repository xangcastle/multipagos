from django.contrib import admin
from django.contrib.admin import site
import adminactions.actions as actions
from import_export.admin import ImportExportModelAdmin
from .models import *
from .resources import *
from django.template.context import RequestContext
from django.shortcuts import render_to_response, HttpResponseRedirect
from .views import *
from digitalizacion.models import *
from django import forms
from django.core.context_processors import csrf
from digitalizacion.api import generar_paginas
actions.add_to_site(site)


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
    resource_class = paquete_resouce

    search_fields = ('factura', 'contrato', 'cliente', 'barra')

    list_display = ('factura', 'contrato', 'cliente', 'iddepartamento',
        'idmunicipio', 'idbarrio', 'exportado', 'entrega',
        'ciclo', 'mes', 'ano', 'link_comprobante')

    list_filter = ('iddepartamento', 'idmunicipio', 'exportado', 'entrega',
        'ciclo', 'mes', 'ano', 'entrega_numero')

    #list_editable = ('comprobante',)
    fieldsets = (('Datos Generales', {
                'classes': ('grp-collapse grp-open',),
                'fields': (('factura', 'cliente', 'contrato'),
                            ('ciclo', 'mes', 'ano'),
                            ('iddepartamento', 'idmunicipio', 'barrio'),
                            ('direccion', 'lote'),
                            ('telefono_contacto', 'ruta', 'zona'))}),
                ('Datos de Facturacion', {
                'classes': ('grp-collapse grp-open',),
                'fields': (('segmento', 'tarifa', 'servicio'),
                            ('cupon', 'total_mes_factura', 'valor_pagar'),
                            ('numero_fiscal', 'factura_interna', 'entrega'))}),
                ('Entrega y Digitalizacion', {
                'classes': ('grp-collapse grp-open',),
                'fields': (('comprobante', 'colector'),
                            ('archivo', 'consecutivo'),
                            ('parentezco', 'recibe', 'fecha_entrega'),
                            'position')}))
    raw_id_fields = ('iddepartamento', 'idmunicipio')
    autocomplete_lookup_fields = {
        'fk': ['iddepartamento', 'idmunicipio'],
        }
    readonly_fields = ('factura', 'cliente', 'contrato', 'cupon', 'ciclo',
        'mes', 'ano', 'departamento', 'municipio', 'barrio', 'direccion',
        'telefono_contacto', 'ruta', 'zona', 'segmento', 'tarifa', 'servicio',
        'cupon', 'total_mes_factura', 'valor_pagar', 'numero_fiscal',
        'factura_interna', 'entrega', 'lote', 'colector')
    actions = ['action_integrar', 'action_lotificar', 'action_imprimir',
        'action_exportar', 'generar_pods']

    change_list_template = 'admin/metropolitana/paquete/change_list.html'

    def action_lotificar(self, request, queryset):
        lotificar(queryset)
    action_lotificar.short_description = 'lotificar facturas seleccionadas'

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


class facturas_asignadas(base_tabular):
    model = Paquete
    fields = ('factura', 'cliente', 'comprobante', 'tipificacion',
        'telefono_contacto')
    readonly_fields = ('factura', 'cliente', 'telefono_contacto')
    ordering = ('cliente', )
    #sortable_field_name = 'consecutivo'


class lote_admin(ImportExportModelAdmin):
    date_hierarchy = 'fecha'
    search_fields = ('numero', 'colector__name', 'departamento__name',
        )
    list_display = ('numero', 'municipio', 'departamento', 'barrio',
        'cerrado', 'cantidad_paquetes', 'entregados', 'avance', 'asignado',
        'colector', 'ciclo', 'mes', 'ano')
    list_filter = ('municipio', 'departamento', 'asignado', 'colector',
        'ciclo', 'mes', 'ano')

    fieldsets = (
        ('Datos del Lote', {'classes': ('grp-collapse grp-open',),
            'fields': (('numero', 'colector'), ('municipio', 'departamento'),
                'barrio', ('cantidad_paquetes', 'entregados', 'avance'))}),
                )

    readonly_fields = ('numero', 'municipio', 'departamento', 'barrio',
        'cantidad_paquetes', 'entregados', 'avance')
    inlines = [facturas_asignadas]
    #actions = ['generar_comprobantes']

    def generar_comprobantes(self, request, queryset):
        paginas = []
        id_unico = False
        if queryset.count() == 1:
            id_unico = True
        comprobantes = Paquete.objects.filter(
            lote__in=queryset).order_by('lote', 'consecutivo')
        if comprobantes:
            pagina = {'comprobantes': []}
            for c in comprobantes:
                pagina['comprobantes'].append(c)
                if len(pagina['comprobantes']) == 4:
                    paginas.append(pagina)
                    pagina = {'comprobantes': []}
            if len(pagina['comprobantes']) > 0:
                paginas.append(pagina)
        ctx = {'queryset': queryset, 'id_unico': id_unico, 'paginas': paginas}
        return render_to_response('metropolitana/comprobante.html',
            ctx, context_instance=RequestContext(request))
    generar_comprobantes.short_description = \
    "Generar comprobantes de los lotes selecionados"


class estadistica_departamento(base_tabular):
    model = EstadisticaDepartamento
    fields = ('departamento', 'total', 'entregados', 'pendientes')
    readonly_fields = ('departamento', 'total', 'entregados', 'pendientes')


class estadistica_ciclo(admin.ModelAdmin):
    list_display = ('code', 'ano', 'mes', 'ciclo', 'total', 'entregados',
        'en_carpeta', 'pendientes', 'rendidos', 'rendiciones', 'por_rendir',
        'cumplimiento', 'alertas')
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
        'generar_rendicion', 'generar_pods']
    inlines = [estadistica_departamento]

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

    def generar_rendicion(self, request, queryset):
        form = None
        if 'apply' in request.POST:
            form = self.numero_rendicion(request.POST)
            if form.is_valid():
                numero = form.cleaned_data['numero']
                for c in queryset:
                    crear_rendicion(c.paquetes().filter(
                        entrega_numero__in=numero))

                self.message_user(request, "rendiciones generadas")
                return HttpResponseRedirect(request.get_full_path())
        if not form:
            form = self.numero_rendicion(
                initial={
                    '_selected_action': request.POST.getlist(
                        admin.ACTION_CHECKBOX_NAME)})
        data = {'ciclos': queryset, 'form': form}
        data.update(csrf(request))
        return render_to_response('metropolitana/numero_rendicion.html', data)

    generar_rendicion.short_description = \
    "Generar rendicion de los ciclos seleccionados"

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
            #response = PDFTemplateResponse(request=request,
                                   #template='metropolitana/comprobante.html',
                                   #filename="comprobantes.pdf",
                                   #context=ctx,
                                   #show_content_in_browser=False,
                                   #)
            #return render_to_pdf_response(request,
                #'metropolitana/comprobante.html', ctx)
            #template = loader.get_template('metropolitana/comprobante.html')
            #html = template.render(Context(ctx))
            #html.encode("UTF-8")
            #result = StringIO.StringIO()
            #pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result, path= settings.RUTA_PROYECTO)

        #if not pdf.err:
            #return HttpResponse(result.getvalue(), content_type='application/pdf')
        #return HttpResponse('<pre>%s</pre>' % escape(html))

        class Media:
            js = ("/static/metropolitana/js/estadistica.js",)



class tipificacion_admin(ImportExportModelAdmin):
    list_display = ('causa', 'descripcion')


class barrio_admin(entidad_admin):
    list_display = ('code', 'name', 'municipio', 'departamento')
    list_filter = ('departamento', 'municipio')


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
    list_display = ('code', 'name', 'municipio', 'departamento')
    list_filter = ('departamento', )
    search_fields = ('departamento__name', 'municipio__name')
    inlines = [zona_barrio_admin]
    readonly_fields = ('code', )
    fields = (('code', 'name'), ('departamento', 'municipio'))


admin.site.register(Paquete, paquete_admin)
admin.site.register(Lote, lote_admin)
admin.site.register(EstadisticaCiclo, estadistica_ciclo)
admin.site.register(Tipificacion, tipificacion_admin)
admin.site.register(Barrio, barrio_admin)
admin.site.register(Municipio, municipio_admin)
admin.site.register(Departamento, entidad_admin)
admin.site.register(Zona, zona_admin)
