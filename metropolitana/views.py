from django.views.generic.base import TemplateView
import json
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from .models import *
from digitalizacion.models import *
from cartera.models import *
from verificaciones.models import *
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import *
from movil.models import UserProfile
from django.contrib.auth.models import User
from cartera.models import import_model


def home(request):
    return HttpResponseRedirect("/admin")


class indexar(TemplateView):
    template_name = "metropolitana/pods.html"


class verificacion_paquete(TemplateView):
    template_name = "metropolitana/verificacion.html"


class entrega_paquete(TemplateView):
    template_name = "metropolitana/entrega.html"


def datos_paquete_(request):

    if request.method == 'GET':
        p = Paquete()
        try:
            p = Paquete.objects.get(barra=request.GET.get('barra', ''))
            datos = {'cliente': p.cliente, 'departamento': p.departamento,
                'municipio': p.municipio, 'lote': 23,
                'cantidad': 5, 'clase': estado(p)[0],
                'valor': estado(p)[1]}
            i = Impresion(paquete=p, user=request.user)
            i.save()
        except p.DoesNotExist:
            datos = {'cliente': 'nada'}
        resp = HttpResponse(json.dumps(datos),
            content_type='application/json')
        resp["Access-Control-Allow-Origin"] = "*"
        resp["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        resp["Access-Control-Allow-Headers"] = "X-Requested-With"
        return resp
    else:
        datos = {'nombre': 'nada'}
        resp = HttpResponse(json.dumps(datos),
            content_type='application/json')
        resp["Access-Control-Allow-Origin"] = "*"
        resp["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        resp["Access-Control-Allow-Headers"] = "X-Requested-With"
        return resp


from django.core import serializers


def datos_paquete(request):
    p = Paquete()
    try:
        p = Paquete.objects.get(barra=request.GET.get('barra', ''))
        i = Impresion(paquete=p, user=request.user)
        i.save()
    except:
        pass
    data = serializers.serialize('json', [p, ])
    struct = json.loads(data)
    data = json.dumps(struct[0])
    return HttpResponse(data, content_type='application/json')


def descarga(request):
    response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % "1065.pdf"
    response['X-Sendfile'] = "/home/abel/PDF/1075.pdf"
    return response


def calcular_entregas(barrio):
    return Paquete.objects.filter(idbarrio=barrio, estado='PENDIENTE',
        cerrado=False, user__isnull=True).count()


def calcular_cobros(barrio):
    return Detalle.objects.filter(idbarrio=barrio, estado='PENDIENTE',
        user__isnull=True).count()


def calcular_verificaciones(barrio):
    return Verificacion.objects.filter(idbarrio=barrio,
        estado='PENDIENTE', user__isnull=True).count()


def usuarios_asignados(zona):
    usuarios = []
    perfiles = UserProfile.objects.all()
    for p in perfiles:
        if zona in p.zonas.all():
            usuarios.append(p.user)
    return usuarios


@csrf_exempt
def get_zonas(request):
    zona_id = int(request.POST.get('zona_id', ''))
    data = []
    z = Zona.objects.get(id=zona_id)
    obj_json = {}
    obj_json['pk'] = z.id
    obj_json['code'] = z.code
    obj_json['name'] = z.name
    barrios = []
    for b in z.barrios():
        if calcular_entregas(b) + calcular_cobros(b) + \
        calcular_verificaciones(b) > 0:
            bar_json = {}
            bar_json['pk'] = b.id
            bar_json['code'] = b.code
            bar_json['name'] = b.name
            bar_json['entregas'] = calcular_entregas(b)
            bar_json['cobros'] = calcular_cobros(b)
            bar_json['verificaciones'] = calcular_verificaciones(b)
            barrios.append(bar_json)
    obj_json['barrios'] = barrios
    data.append(obj_json)
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def get_users_zona(request):
    zona_id = int(request.POST.get('zona_id', ''))
    z = Zona.objects.get(id=zona_id)
    data = serializers.serialize('json', usuarios_asignados(z))
    struct = json.loads(data)
    data = json.dumps(struct)
    return HttpResponse(data, content_type='application/json')


@login_required(login_url='/admin/login/')
def asignacion_paquete(request):
    context = RequestContext(request)
    data = {'zonas': Zona.objects.all().order_by('name'),
        'mensaje': 'En esta seccion usted podra asignar las distintas tareas'
        + ' en cada barrio al gestor hasta una cantidad maxima de x entregas',
        'msgclass': 'info'}
    template_name = "metropolitana/asignacion.html"
    if request.method == "POST":
        t = len(request.POST.getlist('barrio', ''))
        u = User.objects.get(id=int(request.POST.get('usuario', '')))
        fecha = request.POST.get('fecha', '')
        for n in range(0, t):
            idb = int(request.POST.getlist('barrio', '0')[n])
            b = Barrio.objects.get(id=idb)
            try:
                entregas = int(request.POST.getlist('entrega', '0')[n])
            except:
                entregas = None
            try:
                cobros = int(request.POST.getlist('cobro', '0')[n])
            except:
                cobros = None
            try:
                verificaciones = int(request.POST.getlist(
                    'verificacion', '0')[n])
            except:
                verificaciones = None
            if entregas > 0:
                asignar_facturas(b, u, entregas, fecha)
            if cobros > 0:
                asignar_cobros(b, u, cobros, fecha)
            if verificaciones > 0:
                asignar_verificaciones(b, u, verificaciones, fecha)
        data['mensaje'] = 'Tarea asignada con exito!'
        data['msgclass'] = 'success'

    return render_to_response(template_name, data, context_instance=context)


def asignar_facturas(barrio, user, cantidad, fecha):
    ps = Paquete.objects.filter(estado='PENDIENTE', cerrado=False,
        idbarrio=barrio)[:cantidad]
    for p in ps:
        p.user = user
        p.fecha_asignacion_user = fecha
        p.save()
    return ps


def asignar_cobros(barrio, user, cantidad, fecha):
    ps = Detalle.objects.filter(estado='PENDIENTE',
        idbarrio=barrio)[:cantidad]
    for p in ps:
        p.user = user
        p.fecha_asignacion_user = fecha
        p.save()
    return ps


def asignar_verificaciones(barrio, user, cantidad, fecha):
    ps = Verificaciones.objects.filter(estado='PENDIENTE',
        idbarrio=barrio)[:cantidad]
    for p in ps:
        p.user = user
        p.fecha_asignacion_user = fecha
        p.save()
    return ps


@login_required(login_url='/admin/login/')
def telecobranza(request):
    template_name = "metropolitana/telecobranza.html"
    data = {}
    context = RequestContext(request)
    if request.method == "POST":
        pass
    return render_to_response(template_name, data, context_instance=context)


def crear_import_model(paquete):
    i = import_model()
    i.suscriptor = paquete.cliente
    i.contrato = paquete.contrato
    i.departamento = paquete.departamento
    i.localida = paquete.municipio
    i.barr_contrato = paquete.barrio
    i.servicio = paquete.servicio
    i.factura = paquete.factura
    i.no_cupon = paquete.cupon
    i.ciclo = paquete.ciclo
    i.ano = paquete.ano
    i.tipo_mora = "AL DIA"
    i.tel_contacto = paquete.tel_contacto
    i.direccion = paquete.direccion
    i.factura_interna = paquete.factura_interna
    i.saldo_pend_factura = paquete.total_mes_factura
    i.save()


def cargar_para_cobro(ciclo):
    for p in ciclo.paquetes():
        crear_import_model(p)
