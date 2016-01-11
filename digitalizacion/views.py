from .models import *
from django.shortcuts import render_to_response
from django.template import RequestContext
import json
from django.db.models import Q
from django.http.response import HttpResponse
from metropolitana.indexacion import *
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


@csrf_exempt
def cargar_pod(request):
    data = {'mensaje': "carga correcta"}
    c = request.GET.get('code', '00000000000')
    #print str(c)
    p = comprobacion(c[:-6], c[-6:-4], c[-4:-2], '20' + c[-2:])
    #print p
    if p:
        path = settings.MEDIA_ROOT + str(
            request.GET.get('path', '')).replace('media/', '')
        #print path
        p = cargar_comprobante(p, path)
        p.indexacion = int(request.GET.get('id', ''))
        p.exportado = False
        p.save()
    else:
        data['mensaje'] = "carga_incorrecta"
    return HttpResponse(json.dumps(data), content_type='application/json')


def carga_manual(request, id):
    i = Indexacion.objects.get(id=id)
    base = i.url()
    archivos = i.pendientes()
    data = []
    for a in archivos:
        p = os.path.join(base, a)
        data.append(p)
    return render_to_response("metropolitana/carga_manual.html",
        {'archivos': data, 'id': i.id},
        context_instance=RequestContext(request))


def autocomplete_pod(request):
    if request.is_ajax:
        model = Pod
        result = []

        qs = model.objects.filter(
            Q(barra__istartswith=request.GET.get('term', ''))
            )
        for obj in qs:
            obj_json = {}
            obj_json['label'] = str('%s | %s' % (
                obj.cliente.encode('ascii', 'ignore'), obj.consecutivo))
            obj_json['value'] = str(obj.name_file())
            result.append(obj_json)

        data = json.dumps(result)
    else:
        data = 'fail'
    return HttpResponse(data, content_type='application/json')
