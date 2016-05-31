from django.views.generic.base import TemplateView
import json
from django.http.response import HttpResponse
from .models import *
from digitalizacion.models import *
from verificaciones.models import *
from django.views.decorators.csrf import csrf_exempt
from .models import *
from movil.models import UserProfile
from cartera.models import import_model as Factura, Gestion, \
TipoGestion


class home(TemplateView):
    template_name = "base/base.html"


def get_entregas(barrio):
    return Paquete.objects.filter(idbarrio=barrio, estado='PENDIENTE',
        cerrado=False, user__isnull=True)


def get_cobros(barrio):
    return Gestion.objects.filter(barrio=barrio, estado='PENDIENTE',
        user__isnull=True,
        tipo_gestion=TipoGestion.objects.get(code='0002'))


def get_cortes(barrio):
    return Gestion.objects.filter(barrio=barrio, estado='PENDIENTE',
        user__isnull=True,
        tipo_gestion=TipoGestion.objects.get(code='0003'))


def get_verificaciones(barrio):
    return Verificacion.objects.filter(idbarrio=barrio,
        estado='PENDIENTE', user__isnull=True)


def calcular_verificaciones(barrio):
    return get_verificaciones(barrio).count()


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
        calcular_verificaciones(b) + calcular_cortes(b) > 0:
            bar_json = {}
            bar_json['pk'] = b.id
            bar_json['code'] = b.code
            bar_json['name'] = b.name
            bar_json['entregas'] = calcular_entregas(b)
            bar_json['cobros'] = calcular_cobros(b)
            bar_json['cortes'] = calcular_cortes(b)
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


def asignar_facturas(barrio, user, cantidad, fecha):
    ps = get_entregas(barrio)[:cantidad]
    for p in ps:
        p.user = user
        p.fecha_asignacion_user = fecha
        p.save()
    return ps


def asignar_cobros(barrio, user, cantidad, fecha):
    ps = get_cobros(barrio)[:cantidad]
    for p in ps:
        p.user = user
        p.fecha_asignacion = fecha
        p.save()
    return ps


def asignar_cortes(barrio, user, cantidad, fecha):
    print('print asignando cortes')
    ps = get_cortes(barrio)[:cantidad]
    for p in ps:
        p.user = user
        p.fecha_asignacion = fecha
        p.save()
    return ps


def asignar_verificaciones(barrio, user, cantidad, fecha):
    ps = get_verificaciones(barrio)[:cantidad]
    for p in ps:
        p.user = user
        p.fecha_asignacion_user = fecha
        p.save()
    return ps


def crear_import_model(paquete, fecha_fac, fecha_venc, fecha_asig, fecha_fin):
    i, created = Factura.objects.get_or_create(no_cupon=paquete.cupon)
    i.suscriptor = paquete.cliente
    i.contrato = paquete.contrato
    i.departamento = paquete.departamento
    i.localidad = paquete.municipio
    i.barr_contacto = paquete.barrio
    i.iddepartamento = paquete.iddepartamento
    i.idmunicipio = paquete.idmunicipio
    i.idbarrio = paquete.idbarrio
    i.servicio = paquete.servicio
    i.factura = paquete.factura
    i.factura_interna = paquete.factura_interna
    i.no_cupon = paquete.cupon
    i.mes = paquete.mes
    i.ciclo = paquete.ciclo
    i.ano = paquete.ano
    i.tipo_mora = 'AL_DIA'
    i.tel_contacto = paquete.get_telefono()
    i.direccion = paquete.direccion
    i.saldo_pend_factura = paquete.total_mes_factura
    i.comentario = "COBRO"
    i.fecha_fact = fecha_fac
    i.fecha_venc = fecha_venc
    i.fecha_asignacion = fecha_asig
    i.descr_plan = paquete.servicio
    i.save()


def cargar_para_cobro(ciclo, fecha_fac, fecha_venc, fecha_asig, fecha_fin):
    for p in ciclo.paquetes():
        crear_import_model(p, fecha_fac, fecha_venc, fecha_asig, fecha_fin)