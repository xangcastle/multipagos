from .models import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
import json


@login_required(login_url='/admin/login/')
def telecobranza(request):
    template_name = "cartera/telecobranza.html"
    if request.method == "GET":
        contrato = request.GET.get('contrato', '')
        context = RequestContext(request)
        data = {
            'resultados': TipoResultado.objects.all().order_by('descripcion'),
            'cliente': Cliente.objects.get(contrato=contrato)
            }
    if request.method == "POST":
        pass

    return render_to_response(template_name, data, context_instance=context)


def grabar_gestion_telefonica(request):
    data = []
    cliente = Cliente.objects.get(contrato=request.POST.get('contrato', ''))
    g = cliente.generar_gestion(TipoGestion.objects.get(code='0001'),
        request.user)
    g.fecha_gestion = datetime.now()
    g.fecha_promesa = request.POST.get('fecha_promesa', '')
    g.tipo_resultado = TipoResultado.objects.get(
        id=int(request.POST.get('tipo_resultado', '')))
    g.observaciones = request.POST.get('observaciones', '')
    g.save()
    result = model_to_dict(g)
    data = json.dumps(result)
    print(data)
    return HttpResponse(data, content_type='application/json')