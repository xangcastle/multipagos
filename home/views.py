from django.views.generic.base import TemplateView
from metropolitana.models import Barrio, Zona
import json
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from movil.models import UserProfile
from django.contrib.auth.models import User
from metropolitana.views import asignar_facturas, asignar_cobros, \
asignar_verificaciones


class index(TemplateView):
    template_name = "home/base.html"


class barrios_huerfanos(TemplateView):
    template_name = "home/barrios_huerfanos.html"


class reporte_gestiones(TemplateView):
    template_name = "home/gestiones.html"


class panel_asignacion(TemplateView):
    template_name = "home/asignaciones.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['mensaje'] = \
        'En esta seccion usted podra asignar las distintas tareas'
        context['mensaje'] += \
        ' en cada barrio a un gestor que trabaje en la zona elegida'
        context['msgclass'] = 'info'
        context['profile'] = UserProfile.objects.get(user=request.user)
        context['zonas'] = Zona.objects.filter(
            departamento__in=context['profile'].departamentos.all()
            ).order_by('name')
        return super(panel_asignacion, self).render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['profile'] = UserProfile.objects.get(user=request.user)
        context['zonas'] = Zona.objects.filter(
            departamento__in=context['profile'].departamentos.all()
            ).order_by('name')
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
    result = []
    if request.is_ajax:
        barrio = Barrio.objects.get(id=request.POST.get('idbarrio', None))
        zona = Zona.objects.get(id=request.POST.get('idzona', None))
        zona.add_barrio(barrio)
    data = json.dumps(model_to_dict(zona))
    return HttpResponse(data, content_type='application/json')
