from django.views.generic.base import TemplateView
import json
from django.http.response import HttpResponse
from .models import *
from digitalizacion.models import *
#    from django.shortcuts import render_to_response
#from django.forms.models import model_to_dict


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
