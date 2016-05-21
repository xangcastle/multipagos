from django.views.generic.base import TemplateView
from metropolitana.models import Barrio, Zona
import json
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from movil.models import UserProfile
from django.contrib.auth.models import User
from cartera.models import Gestion, TipoGestion
from metropolitana.models import Paquete
from verificaciones.models import Verificacion
from django.core import serializers
from datetime import date, datetime


class index(TemplateView):
    template_name = "home/base.html"


class barrios_huerfanos(TemplateView):
    template_name = "home/barrios_huerfanos.html"


def get_entregas(barrios):
    return Paquete.objects.filter(idbarrio__in=barrios, estado='PENDIENTE',
        cerrado=False, user__isnull=True)


def calcular_entregas(barrios):
    return get_entregas(barrios).count()


def get_cobros(barrios):
    return Gestion.objects.filter(barrio__in=barrios, estado='PENDIENTE',
        user__isnull=True,
        tipo_gestion=TipoGestion.objects.get(code='0002'))


def calcular_cobros(barrios):
    return get_cobros(barrios).count()


def get_verificaciones(barrios):
    return Verificacion.objects.filter(idbarrio__in=barrios,
        estado='PENDIENTE', user__isnull=True)


def calcular_verificaciones(barrios):
    return get_verificaciones(barrios).count()


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
        barrio = Barrio.objects.filter(id__in=[b.id, ])
        if calcular_entregas(b) + calcular_cobros(b) + \
        calcular_verificaciones(b) > 0:
            bar_json = {}
            bar_json['pk'] = b.id
            bar_json['code'] = b.code
            bar_json['name'] = b.name
            bar_json['entregas'] = calcular_entregas(barrio)
            bar_json['cobros'] = calcular_cobros(barrio)
            bar_json['verificaciones'] = calcular_verificaciones(barrio)
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


class panel_asignacion(TemplateView):
    template_name = "home/asignaciones.html"

    def get_profile(self, user):
        try:
            return UserProfile.objects.get(user=user)
        except:
            profile, created = UserProfile.objects.get_or_create(
                is_supervisor=False, user=user)
            profile.save()
            return profile

    def get_zonas(self, context):
        data = []
        zonas = Zona.objects.filter(
            departamento__in=context['profile'].departamentos.all()
            ).order_by('name')
        for z in zonas:
            o = model_to_dict(z)
            o['entregas'] = calcular_entregas(z.barrios())
            o['cobros'] = calcular_cobros(z.barrios())
            o['verificaciones'] = calcular_verificaciones(z.barrios())
            o['total'] = o['entregas'] + o['cobros'] + o['verificaciones']
            data.append(o)
        return data

    def get_extra_context(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['profile'] = self.get_profile(request.user)
        context['zonas'] = self.get_zonas(context)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_extra_context(request, *args, **kwargs)
        return super(panel_asignacion, self).render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_extra_context(request, *args, **kwargs)
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
        context['mensaje'] = 'Tarea asignada con exito!'
        context['msgclass'] = 'success'
        return super(panel_asignacion, self).render_to_response(context)


def asignar_facturas(barrio, user, cantidad, fecha):
    b = Barrio.objects.filter(id__in=[barrio.id, ])
    ps = get_entregas(b)[:cantidad]
    for p in ps:
        p.user = user
        p.fecha_asignacion_user = fecha
        p.save()
    return ps


def asignar_cobros(barrio, user, cantidad, fecha):
    b = Barrio.objects.filter(id__in=[barrio.id, ])
    ps = get_cobros(b)[:cantidad]
    for p in ps:
        p.user = user
        p.fecha_asignacion = fecha
        p.save()
    return ps


def asignar_verificaciones(barrio, user, cantidad, fecha):
    b = Barrio.objects.filter(id__in=[barrio.id, ])
    ps = get_verificaciones(b)[:cantidad]
    for p in ps:
        p.user = user
        p.fecha_asignacion_user = fecha
        p.save()
    return ps


@csrf_exempt
def info_barrio(request):
    if request.is_ajax:
        result = []
        obj = Barrio.objects.get(id=request.POST.get('id', None))
        if obj:
            try:
                result = obj.to_json()
            except:
                result = model_to_dict(obj)
            data = json.dumps(result)
    else:
        data = []
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def asignar_barrio(request):
    if request.is_ajax:
        barrio = Barrio.objects.get(id=request.POST.get('idbarrio', None))
        zona = Zona.objects.get(id=request.POST.get('idzona', None))
        zona.add_barrio(barrio)
    data = json.dumps(model_to_dict(zona))
    return HttpResponse(data, content_type='application/json')


class carga_informacion(TemplateView):
    template_name = "home/carga.html"


class reporte_gestiones(TemplateView):
    template_name = "home/gestiones.html"

    def get_profile(self, user):
        try:
            return UserProfile.objects.get(user=user)
        except:
            profile, created = UserProfile.objects.get_or_create(
                is_supervisor=False, user=user)
            profile.save()
            return profile
##PENDIENTE

    def pendiente_distribucion(self, user):
        return Paquete.objects.filter(user=user, estado='PENDIENTE',
            fecha_asignacion_user__lte=date.today())

    def pendiente_cobros(self, user):
        return Gestion.objects.filter(user=user, estado="PENDIENTE",
            tipo_gestion=TipoGestion.objects.get(code="0002"),
            fecha_asignacion__lte=date.today())

    def pendiente_cortes(self, user):
        return Gestion.objects.filter(user=user, estado="PENDIENTE",
            tipo_gestion=TipoGestion.objects.get(code="0003"),
            fecha_asignacion__lte=date.today())

    def pendiente_verificaciones(self, user):
        return Verificacion.objects.filter(user=user, estado='PENDIENTE',
            fecha_asignacion__lte=date.today())
##REALIZADO

    def realizado_distribucion(self, user):
        return Paquete.objects.filter(user=user,
            fecha_entrega__day=datetime.now().day,
            fecha_entrega__month=datetime.now().month,
            fecha_entrega__year=datetime.now().year)

    def realizado_cobros(self, user):
        return Gestion.objects.filter(user=user,
            tipo_gestion=TipoGestion.objects.get(code="0002"),
            fecha_gestion__day=datetime.now().day,
            fecha_gestion__month=datetime.now().month,
            fecha_gestion__year=datetime.now().year)

    def realizado_cortes(self, user):
        return Gestion.objects.filter(user=user,
            tipo_gestion=TipoGestion.objects.get(code="0003"),
            fecha_gestion__day=datetime.now().day,
            fecha_gestion__month=datetime.now().month,
            fecha_gestion__year=datetime.now().year)

    def realizado_verificaciones(self, user):
        return Verificacion.objects.filter(user=user,
            fecha_entrega__day=datetime.now().day,
            fecha_entrega__month=datetime.now().month,
            fecha_entrega__year=datetime.now().year)

##ASIGNADO

    def asignado_distribucion(self, user):
        return Paquete.objects.filter(user=user,
            fecha_asignacion_user__lte=date.today())

    def asignado_cobros(self, user):
        return Gestion.objects.filter(user=user,
            tipo_gestion=TipoGestion.objects.get(code="0002"),
            fecha_asignacion__lte=date.today())

    def asignado_cortes(self, user):
        return Gestion.objects.filter(user=user,
            tipo_gestion=TipoGestion.objects.get(code="0003"),
            fecha_asignacion__lte=date.today())

    def asignado_verificaciones(self, user):
        return Verificacion.objects.filter(user=user,
            fecha_asignacion__lte=date.today())

    def user_pendiente(self, user):
        asignacion = {}
        asignacion['distribucion'] = self.pendiente_distribucion(user).count()
        asignacion['cobros'] = self.pendiente_cobros(user).count()
        asignacion['cortes'] = self.pendiente_cortes(user).count()
        asignacion['verificaciones'] = \
        self.pendiente_verificaciones(user).count()
        asignacion['total'] = asignacion['distribucion'] + \
        asignacion['cobros'] + asignacion['cortes'] + \
        asignacion['verificaciones']
        return asignacion

    def user_realizado(self, user):
        asignacion = {}
        asignacion['distribucion'] = self.realizado_distribucion(user).count()
        asignacion['cobros'] = self.realizado_cobros(user).count()
        asignacion['cortes'] = self.realizado_cortes(user).count()
        asignacion['verificaciones'] = \
        self.realizado_verificaciones(user).count()
        asignacion['total'] = asignacion['distribucion'] + \
        asignacion['cobros'] + asignacion['cortes'] + \
        asignacion['verificaciones']
        return asignacion

    def user_asignado(self, user):
        asignacion = {}
        asignacion['distribucion'] = self.asignado_distribucion(user).count()
        asignacion['cobros'] = self.asignado_cobros(user).count()
        asignacion['cortes'] = self.asignado_cortes(user).count()
        asignacion['verificaciones'] = \
        self.asignado_verificaciones(user).count()
        asignacion['total'] = asignacion['distribucion'] + \
        asignacion['cobros'] + asignacion['cortes'] + \
        asignacion['verificaciones']
        return asignacion

    def user_estadisticas(self, user):
        asignacion = {}
        asignacion['pendiente'] = self.user_pendiente(user)
        asignacion['realizado'] = self.user_realizado(user)
        asignacion['asignado'] = self.user_asignado(user)
        asignacion['total'] = asignacion['pendiente']['total'] + \
        asignacion['realizado']['total'] + \
        asignacion['asignado']['total']
        asignacion['cumplimiento'] = round((
            asignacion['realizado']['total'] * 100) /
        asignacion['total'], 0)
        return asignacion

    def get_users(self, context):
        users = []
        data = []
        zonas = Zona.objects.filter(
            departamento__in=context['profile'].departamentos.all()
            ).order_by('name')
        for z in zonas:
            for u in usuarios_asignados(z):
                users.append(u.id)
        for u in User.objects.filter(id__in=users):
            obj = {}
            obj['user'] = u
            obj['profile'] = self.get_profile(u)
            obj['estadisticas'] = self.user_estadisticas(u)
            data.append(obj)
        return data

    def get_extra_context(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['profile'] = self.get_profile(request.user)
        context['gestores'] = self.get_users(context)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_extra_context(request, *args, **kwargs)
        return super(reporte_gestiones, self).render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_extra_context(request, *args, **kwargs)
        return super(reporte_gestiones, self).render_to_response(context)