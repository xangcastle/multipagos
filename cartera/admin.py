from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
from .resources import *
from django import forms
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect


class import_model_admin(ImportExportModelAdmin):
    list_display = ('contrato', 'suscriptor', 'comentario', 'servicio',
        'departamento', 'localidad', 'barr_contacto', 'servicio',
        'saldo_pend_factura', 'ciclo', 'mes', 'ano')

    def action_integrar(self, request, queryset):
        for q in queryset:
            q.integrar()
        self.message_user(request, "integracion de registros exitosa")
    action_integrar.short_description = \
    "actualizar cartera mora y rebajas"

    actions = [action_integrar]

admin.site.register(import_model, import_model_admin)


class base_tabular(admin.TabularInline):
    extra = 0
    classes = ('grp-collapse grp-open',)


class detalle_cartera(base_tabular):
    model = Factura
    fields = ('factura', 'factura_interna', 'no_cupon', 'no_fiscal',
        'fecha_fact', 'fecha_venc', 'tipo_mora', 'saldo_pend_factura', 'saldo')
    readonly_fields = ('factura', 'factura_interna', 'no_cupon', 'no_fiscal',
        'fecha_fact', 'fecha_venc', 'tipo_mora', 'saldo_pend_factura', 'saldo')

class usuarios_asignados(base_tabular):
    model = AsignacionCliente
    fields = ('user', 'tipo_gestion')


class cliente_admin(admin.ModelAdmin):
    list_display = ('contrato', 'name', 'identificacion', 'saldo_total',
        'comentario', 'tipo_mora', 'ciclo', 'departamento', 'municipio',
        'barrio', 'zona', 'estado_corte')
    list_filter = ('departamento', 'municipio', 'barrio',
        'tipo_mora', 'ciclo', 'comentario', 'zona', 'estado_corte', 'has_pend')
    search_fields = ('code', 'name', 'identificacion', 'contrato')
    readonly_fields = ('code', 'name', 'identificacion', 'departamento',
        'municipio', 'barrio', 'zona', 'comentario', 'direccion', 'tipo_mora',
        'telefonos', 'saldo_total', 'ciclo', 'estado_corte',
        'fecha_instalacion', 'descr_plan', 'tecnologia', 'canal_venta',
        'ejecutivo_venta', 'facturas_generadas', 'facturas_pagadas', 'contrato')
    fieldsets = (
        ('Datos Generales', {
                'classes': ('grp-collapse grp-open', ),
                'fields': (
                            ('name', 'contrato'), ('code', 'identificacion'),
                            ('departamento', 'municipio', 'barrio', 'zona'),
                            ('telefonos', 'tipo_mora', 'comentario'),
                            'direccion', ('saldo_total', 'ciclo',
                                'estado_corte', 'fecha_instalacion'),
                            ('descr_plan', 'tecnologia', 'canal_venta',
                                'ejecutivo_venta'), ('facturas_generadas',
                                'facturas_pagadas'),
                        )
        }),
        ("Detalle de Mora", {"classes":
            ("placeholder factura_set-group",), "fields": ()}),
        #('Ubicacion Exacta', {
                #'classes': ('grp-collapse grp-open', ),
                #'fields': ('position', )
        #}),
                            )
    inlines = [detalle_cartera, usuarios_asignados]

    actions = ['action_orden_corte', 'generar_gestion']

    def action_orden_corte(self, request, queryset):
        for obj in queryset:
            obj.generar_orden_corte()
    action_orden_corte.short_description = \
    "generar orden de corte para los clientes seleccionados"

    class tipo_gestion(forms.Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        tipo = forms.ModelChoiceField(
            queryset=TipoGestion.objects.all().order_by('code'))

    def generar_gestion(self, request, queryset):
        form = None
        if 'apply' in request.POST:
            form = self.tipo_gestion(request.POST)
            if form.is_valid():
                tipo = form.cleaned_data['tipo']
                print(tipo)
                for c in queryset:
                    c.generar_gestion(tipo)
                self.message_user(request, "Gestiones generadas con exito")
                return HttpResponseRedirect("/admin/cartera/cliente")
            else:
                self.message_user(request, "accion invalida")
                data = {'clientes': queryset, 'form': form}
                return render_to_response('metropolitana/tipo_gestion.html',
                    data)
        if not form:
            form = self.tipo_gestion(
                initial={
                    '_selected_action': request.POST.getlist(
                        admin.ACTION_CHECKBOX_NAME)})
        data = {'clientes': queryset, 'form': form}
        data.update(csrf(request))
        return render_to_response('metropolitana/tipo_gestion.html', data)

admin.site.register(Cliente, cliente_admin)


class tipo_gestion_admin(admin.ModelAdmin):
    list_display = ('code', 'name')


admin.site.register(TipoGestion, tipo_gestion_admin)


class tipo_mora_admin(admin.ModelAdmin):
    list_display = ('name', 'dias')


admin.site.register(TipoMora, tipo_mora_admin)


class gestion_admin(admin.ModelAdmin):
    date_hierarchy = "fecha_gestion"
    list_display = ('cliente', 'departamento', 'municipio', 'barrio',
        'tipo_gestion', 'fecha_asignacion', 'fecha_vencimiento',
        'fecha_gestion', 'tipo_resultado', 'user', 'estado')
    list_filter = ('departamento', 'municipio', 'barrio', 'tipo_gestion',
        'estado', 'user')

    search_fields = ('cliente__name', 'cliente__contrato', 'user__username')

admin.site.register(Gestion, gestion_admin)


class resultado_admin(admin.ModelAdmin):
    list_display = ('signo', 'descripcion', 'resultado')


admin.site.register(TipoResultado, resultado_admin)