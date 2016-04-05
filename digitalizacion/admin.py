from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import math
from metropolitana.models import exportar_media_temp, Paquete
from metropolitana.indexacion import indexar_carpeta


class pod_admin(admin.ModelAdmin):
    list_display = ('factura', 'contrato', 'consecutivo', 'cliente',
        'ciclo', 'mes', 'entrega', 'comprobante')
    list_editable = ('comprobante',)
    search_fields = ('factura', 'contrato', 'cliente', 'barra')
    list_filter = ('ano', 'mes', 'ciclo', 'entrega', 'departamento', 'archivo',
        'entrega_numero')
    actions = ['action_exportar']

    def action_exportar(self, request, queryset):
        ps = Paquete.objects.filter(id__in=queryset.values_list('id',
        flat=True))
        exportar_media_temp(ps)
    action_exportar.short_description = 'exportar pdf de pods seleccionados'


class impresion_admin(ImportExportModelAdmin):
    date_hierarchy = 'fecha_verificacion'
    list_display = ('consecutivo', 'paquete', 'cliente', 'user',
        'archivo', 'fecha_verificacion')
    list_per_page = 1200
    list_filter = ('user', 'archivo')
    search_fields = ('paquete__cliente', 'paquete__factura', 'paquete__barra',
        'paquete__contrato')
    actions = ['generar_comprobantes']

    def generar_comprobantes(self, request, queryset):
        paginas = []
        id_unico = False
        if queryset.count() == 1:
            id_unico = True
        for q in queryset:
            c = Paquete.objects.get(id=q.paquete.id)
            c.orden_impresion = q.consecutivo
            c.save()
        comprobantes = Paquete.objects.filter(
            id__in=queryset.order_by('consecutivo').values_list('paquete',
                flat=True)).order_by('archivo', 'orden_impresion')
        if comprobantes:
            pagina = {'comprobantes': []}
            tp = int(math.ceil(comprobantes.count() / 6.0))
            for p in range(0, tp):
                for i in range(p, int(tp * 6), tp):
                    try:
                        pagina['comprobantes'].append(comprobantes[i])
                    except:
                        pagina['comprobantes'].append(Paquete())
                if len(pagina['comprobantes']) == 6:
                    paginas.append(pagina)
                    pagina = {'comprobantes': []}
            if len(pagina['comprobantes']) > 0:
                paginas.append(pagina)
        ctx = {'queryset': queryset, 'id_unico': id_unico, 'paginas': paginas}
        return render_to_response('metropolitana/comprobante.html',
            ctx, context_instance=RequestContext(request))
    generar_comprobantes.short_description = \
    "Generar comprobantes selecionados"


admin.site.register(Pod, pod_admin)
admin.site.register(Impresion, impresion_admin)
admin.site.register(import_paquete, ImportExportModelAdmin)


class indexacion_admin(ImportExportModelAdmin):
    date_hierarchy = "fecha"
    list_display = ('fecha', 'total', 'resumen_por_ciclo', 'carga_manual',
        'carpeta', 'path')
    fields = ('archivos', 'make_ocr')
    actions = ['action_indexar']

    def action_indexar(self, request, queryset):
        for obj in queryset:
            indexar_carpeta(obj)
    action_indexar.short_description = \
    'Iniciar proceso de indexacion automatica'

admin.site.register(Indexacion, indexacion_admin)


class empleado_admin(ImportExportModelAdmin):
    list_display = ('idempleado', 'nombre', 'cedula', 'gerencia', 'localidad',
        'link_ecuenta')
    list_filter = ('localidad', )
    search_fields = ('idempleado', 'nombre', 'cedula')

admin.site.register(Empleado, empleado_admin)
admin.site.register(Tar)
