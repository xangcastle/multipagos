import json
from metropolitana.models import Paquete, Zona, Barrio
from verificaciones.models import Verificacion
from cartera.models import Gestion, TipoGestion
from movil.models import UserProfile
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.forms.models import model_to_dict


def get_entregas(barrios):
    return Paquete.objects.filter(idbarrio__in=barrios, estado='PENDIENTE',
        cerrado=False, user__isnull=True)


def get_gestiones(barrios, codigo):
    return Gestion.objects.filter(barrio__in=barrios, estado='PENDIENTE',
        user__isnull=True,
        tipo_gestion=TipoGestion.objects.get(code=codigo))


def get_verificaciones(barrios):
    return Verificacion.objects.filter(idbarrio__in=barrios,
        estado='PENDIENTE', user__isnull=True)


def usuarios_asignados(zona):
    usuarios = []
    perfiles = UserProfile.objects.all()
    for p in perfiles:
        if zona in p.zonas.all():
            usuarios.append(p.user)
    return usuarios


def asignar_facturas(barrio, user, cantidad, fecha):
    barrios = Barrio.objects.filter(id=barrio.id)
    ps = get_entregas(barrios)[:cantidad]
    for p in ps:
        p.user = user
        p.fecha_asignacion_user = fecha
        p.save()
    return ps


def asignar_gestiones(barrio, codigo, user, cantidad, fecha):
    barrios = Barrio.objects.filter(id=barrio.id)
    ps = get_gestiones(barrios, codigo)[:cantidad]
    for p in ps:
        p.user = user
        p.fecha_asignacion = fecha
        p.save()
    return ps


def asignar_verificaciones(barrio, user, cantidad, fecha):
    barrios = Barrio.objects.filter(id=barrio.id)
    ps = get_verificaciones(barrios)[:cantidad]
    for p in ps:
        p.user = user
        p.fecha_asignacion_user = fecha
        p.save()
    return ps


