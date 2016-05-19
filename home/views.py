from django.views.generic.base import TemplateView
from metropolitana.models import Barrio, Zona
import json
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt


class index(TemplateView):
    template_name = "home/base.html"


class barrios_huerfanos(TemplateView):
    template_name = "home/barrios_huerfanos.html"


class reporte_gestiones(TemplateView):
    template_name = "home/gestiones.html"


class panel_asignacion(TemplateView):
    template_name = "home/asignaciones.html"

    def get_context_data(self, **kwargs):
        context = super(panel_asignacion, self).get_context_data(**kwargs)
        context['zonas'] = Zona.objects.all().order_by('name')
        context['mensaje'] = \
        'En esta seccion usted podra asignar las distintas tareas'
        context['mensaje'] += \
        ' en cada barrio al gestor hasta una cantidad maxima de x entregas'
        context['msgclass'] = 'info'
        return context


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
