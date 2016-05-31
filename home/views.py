from django.views.generic.base import TemplateView
from metropolitana.models import Barrio, Zona
from django.forms.models import model_to_dict
from movil.models import UserProfile
from django.contrib.auth.models import User
from cartera.models import Gestion, TipoGestion
from metropolitana.models import Paquete
from verificaciones.models import Verificacion
from datetime import date, datetime
from django.db.models import Q
from .ajax import *


def get_profile(view, user):
    try:
        return UserProfile.objects.get(user=user)
    except:
        profile, created = UserProfile.objects.get_or_create(
            is_supervisor=False, user=user)
        profile.save()
        return profile


def profile_get_zonas(view, context):
    data = []
    zonas = Zona.objects.filter(
        departamento__in=context['profile'].departamentos.all()
        ).order_by('name')
    for z in zonas:
        o = model_to_dict(z)
        o['entregas'] = get_entregas(z.barrios()).count()
        o['cobros'] = get_gestiones(z.barrios(), '0002').count()
        o['cortes'] = get_gestiones(z.barrios(), '0003').count()
        o['verificaciones'] = get_verificaciones(z.barrios()).count()
        o['total'] = o['entregas'] + o['cobros'] + o['verificaciones'] + \
        o['cortes']
        data.append(o)
    return data


def get_extra_context(view, request, *args, **kwargs):
    context = view.get_context_data()
    context['profile'] = get_profile(view, request.user)
    context['zonas'] = profile_get_zonas(view, context)
    return context


class index(TemplateView):
    template_name = "home/base.html"


class barrios_huerfanos(TemplateView):
    template_name = "home/barrios_huerfanos.html"


class panel_asignacion(TemplateView):
    template_name = "home/asignaciones.html"

    def get(self, request, *args, **kwargs):
        context = get_extra_context(self, request, *args, **kwargs)
        return super(panel_asignacion, self).render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = get_extra_context(self, request, *args, **kwargs)
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
            try:
                cortes = int(request.POST.getlist('corte', '0')[n])
            except:
                cortes = None
            if entregas > 0:
                asignar_facturas(b, u, entregas, fecha)
            if cobros > 0:
                asignar_gestiones(b, '0002', u, cobros, fecha)
            if verificaciones > 0:
                asignar_verificaciones(b, u, verificaciones, fecha)
            if cortes > 0:
                asignar_gestiones(b, '0003', u, cortes, fecha)
        context['mensaje'] = 'Tarea asignada con exito!'
        context['msgclass'] = 'success'
        return super(panel_asignacion, self).render_to_response(context)


class carga_informacion(TemplateView):
    template_name = "home/carga.html"

    def get(self, request, *args, **kwargs):
        context = get_extra_context(self, request, *args, **kwargs)
        return super(carga_informacion, self).render_to_response(context)


class reporte_gestiones(TemplateView):
    template_name = "home/gestiones.html"
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
        return Paquete.objects.filter(
            Q(user=user, estado='PENDIENTE', cerrado=False,
            fecha_asignacion_user__lte=date.today()) |
            Q(user=user,
            fecha_entrega__day=datetime.now().day,
            fecha_entrega__month=datetime.now().month,
            fecha_entrega__year=datetime.now().year)
        )

    def asignado_cobros(self, user):
        return Gestion.objects.filter(
            Q(user=user, estado="PENDIENTE",
            tipo_gestion=TipoGestion.objects.get(code="0002"),
            fecha_asignacion__lte=date.today()) |
            Q(user=user,
            tipo_gestion=TipoGestion.objects.get(code="0002"),
            fecha_gestion__day=datetime.now().day,
            fecha_gestion__month=datetime.now().month,
            fecha_gestion__year=datetime.now().year)
        )

    def asignado_cortes(self, user):
        return Gestion.objects.filter(
            Q(user=user, estado="PENDIENTE",
            tipo_gestion=TipoGestion.objects.get(code="0003"),
            fecha_asignacion__lte=date.today()) |
            Q(user=user,
            tipo_gestion=TipoGestion.objects.get(code="0003"),
            fecha_gestion__day=datetime.now().day,
            fecha_gestion__month=datetime.now().month,
            fecha_gestion__year=datetime.now().year))

    def asignado_verificaciones(self, user):
        return Verificacion.objects.filter(
            Q(user=user, estado='PENDIENTE',
            fecha_asignacion__lte=date.today()) |
            Q(user=user,
            fecha_entrega__day=datetime.now().day,
            fecha_entrega__month=datetime.now().month,
            fecha_entrega__year=datetime.now().year)
        )

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

    def calcular_cumplimiento(self, asignado, realizado):
        if asignado < 1:
            return 0.0
        else:
            return round((realizado * 100) / asignado, 1)

    def user_estadisticas(self, user):
        asignacion = {}
        asignacion['pendiente'] = self.user_pendiente(user)
        asignacion['realizado'] = self.user_realizado(user)
        asignacion['asignado'] = self.user_asignado(user)
        asignacion['cumplimiento'] = self.calcular_cumplimiento(
            asignacion['asignado']['total'], asignacion['realizado']['total'])
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
            obj['profile'] = get_profile(self, u)
            obj['estadisticas'] = self.user_estadisticas(u)
            data.append(obj)
        return data

    def get(self, request, *args, **kwargs):
        context = get_extra_context(self, request, *args, **kwargs)
        context['gestores'] = self.get_users(context)
        return super(reporte_gestiones, self).render_to_response(context)

    def post(self, request, *args, **kwargs):
        desasignar(request.POST.getlist('entrega', ''), Paquete)
        desasignar(request.POST.getlist('cobro', ''), Gestion)
        desasignar(request.POST.getlist('corte', ''), Gestion)
        desasignar(request.POST.getlist('verificacion', ''), Verificacion)
        context = get_extra_context(self, request, *args, **kwargs)
        context['gestores'] = self.get_users(context)
        return super(reporte_gestiones, self).render_to_response(context)


def desasignar(selected, model):
    qs = model.objects.filter(id__in=selected)
    qs.update(user=None)


@csrf_exempt
def get_users_zona(request):
    zona_id = int(request.POST.get('zona_id', ''))
    z = Zona.objects.get(id=zona_id)
    data = serializers.serialize('json', usuarios_asignados(z))
    struct = json.loads(data)
    data = json.dumps(struct)
    return HttpResponse(data, content_type='application/json')


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
        bs = Barrio.objects.filter(id=b.id)
        if get_entregas(bs).count() + \
        get_gestiones(bs, '0002').count() + \
        get_gestiones(bs, '0003').count() + \
        get_verificaciones(bs).count():
            bar_json = {}
            bar_json['pk'] = b.id
            bar_json['code'] = b.code
            bar_json['name'] = b.name
            bar_json['entregas'] = get_entregas(bs).count()
            bar_json['cobros'] = get_gestiones(bs, '0002').count()
            bar_json['cortes'] = get_gestiones(bs, '0003').count()
            bar_json['verificaciones'] = get_verificaciones(bs).count()
            barrios.append(bar_json)
    obj_json['barrios'] = barrios
    data.append(obj_json)
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def entregas_pendientes(request):
    ps = reporte_gestiones().pendiente_distribucion(
        User.objects.get(id=int(request.POST.get('usuario', ''))))
    data = serializers.serialize('json',
        ps)
    struct = json.loads(data)
    data = json.dumps(struct)
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def cobros_pendientes(request):
    ps = reporte_gestiones().pendiente_cobros(
        User.objects.get(id=int(request.POST.get('usuario', ''))))
    data = []
    for p in ps:
        obj = {}
        obj['id'] = p.id
        obj['cliente'] = p.cliente.name
        obj['direccion'] = p.cliente.direccion
        data.append(obj)
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def cortes_pendientes(request):
    ps = reporte_gestiones().pendiente_cortes(
        User.objects.get(id=int(request.POST.get('usuario', ''))))
    data = []
    for p in ps:
        obj = {}
        obj['id'] = p.id
        obj['cliente'] = p.cliente.name
        obj['direccion'] = p.cliente.direccion
        data.append(obj)
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def verificaciones_pendientes(request):
    ps = reporte_gestiones().pendiente_verificaciones(
        User.objects.get(id=int(request.POST.get('usuario', ''))))
    data = serializers.serialize('json',
        ps)
    struct = json.loads(data)
    data = json.dumps(struct)
    return HttpResponse(data, content_type='application/json')