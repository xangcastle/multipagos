import json
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.core import serializers
from metropolitana.models import Paquete, Tipificacion, EstadisticaCiclo, \
    Departamento, estadisticas_por_departamento
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from geoposition import Geoposition
from verificaciones.models import Verificacion


@csrf_exempt
def get_user(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username=username, password=password)
    if user:
        data = serializers.serialize('json', [user, ])
        struct = json.loads(data)
        data = json.dumps(struct[0])
    else:
        data = None
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def get_paquetes(request):
    ciclo = request.POST.get('ciclo', '')
    mes = request.POST.get('mes', '')
    ano = request.POST.get('ano', '')
    d = request.POST.get('departamento', '')
    departamento = Departamento.objects.get(id=d)
    queryset = Paquete.objects.filter(ciclo=ciclo, mes=mes, ano=ano,
        iddepartamento=departamento)
    if queryset:
        data = serializers.serialize('json', queryset)
        struct = json.loads(data)
        data = json.dumps(struct)
    else:
        data = None
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def get_paquete(request):
    obj_json = {}
    obj_json['Usuario'] = request.POST.get('Usuario', '')
    obj_json['Motivo'] = request.POST.get('Motivo', '')
    obj_json['Barra'] = request.POST.get('Barra', '')
    obj_json['Fecha'] = str(request.POST.get('Fecha', ''))
    obj_json['Parentezco'] = request.POST.get('Parentezco', '')
    obj_json['Recibe'] = request.POST.get('Recibe', '')
    obj_json['Latitude'] = request.POST.get('Latitude', '')
    obj_json['Longitude'] = request.POST.get('Longitude', '')
    obj_json['Mensaje'] = ''
    try:
        u = User.objects.get(id=int(obj_json['Usuario']))
    except:
        u = None
    try:
        t = Tipificacion.objects.get(id=int(obj_json['Motivo']))
    except:
        t = None
    try:
        p = Paquete.objects.get(barra=obj_json['Barra'])
    except:
        p = None
    if p:
        if p.imagen or p.position:
            m = None
            if p.tipificacion:
                m = p.tipificacion.id
            u = None
            if p.user:
                u = p.user.id
            obj_json['Usuario'] = u
            obj_json['Motivo'] = m
            obj_json['Barra'] = p.barra
            obj_json['Fecha'] = str(p.fecha_entrega)
            obj_json['Parentezco'] = p.parentezco
            obj_json['Recibe'] = p.recibe
            obj_json['Latitude'] = float(p.position.latitude)
            obj_json['Longitude'] = float(p.position.longitude)
            obj_json['Mensaje'] = "Este paquete ya fue cargado"
        else:
            p.user = u
            p.tipificacion = t
            p.fecha_entrega = obj_json['Fecha']
            p.parentezco = obj_json['Parentezco']
            p.recibe = obj_json['Recibe']
            p.position = Geoposition(obj_json['Latitude'],
                obj_json['Longitude'])
            try:
                p.imagen = request.FILES['Imagen']
            except:
                pass
            p.exportado = True
            obj_json['Mensaje'] = "Paquete cargado Correctamente"
            p.save()
    data = json.dumps(obj_json)
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def estadisticasDepartamento(request):
    data = []
    ciclo = request.POST.get('ciclo', '')
    mes = request.POST.get('mes', '')
    ano = request.POST.get('ano', '')
    c = EstadisticaCiclo.objects.get(ciclo=ciclo, mes=mes, ano=ano)
    estadisticas = c.estadisticas_departamentos()
    for e in estadisticas:
        obj_json = {}
        obj_json['departamento'] = e['name']
        obj_json['entregado'] = e['ENTREGADO']
        obj_json['rezagado'] = e['REZAGADO']
        obj_json['pendiente'] = e['PENDIENTE']
        data.append(obj_json)
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def get_departamentos(request):
    ds = Departamento.objects.all().order_by('name')
    data = serializers.serialize('json', ds)
    struct = json.loads(data)
    data = json.dumps(struct)
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def estadisticas_by_user(request):
    ciclo = request.POST.get('ciclo', '')
    mes = request.POST.get('mes', '')
    ano = request.POST.get('ano', '')
    d = request.POST.get('departamento', '')
    departamento = Departamento.objects.get(id=d)
    data = estadisticas_por_departamento(ciclo, mes, ano, departamento)
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def get_verificacion(request):
    obj_json = {}
    obj_json['Usuario'] = request.POST.get('Usuario', '')
    obj_json['Solicitud'] = request.POST.get('Solicitud', '')
    obj_json['Fecha'] = str(request.POST.get('Fecha', ''))
    obj_json['Latitude'] = request.POST.get('Latitude', '')
    obj_json['Longitude'] = request.POST.get('Longitude', '')
    obj_json['Mensaje'] = ''
    try:
        u = User.objects.get(id=int(obj_json['Usuario']))
    except:
        u = None
    try:
        v = Verificacion.objects.get(solicitud=obj_json['Solicitud'])
    except:
        v = None
    if v:
        if v.position:
            obj_json['Usuario'] = u
            obj_json['Solicitud'] = v.solicitud
            obj_json['Fecha'] = str(v.fecha_entrega)
            obj_json['Latitude'] = float(v.position.latitude)
            obj_json['Longitude'] = float(v.position.longitude)
            obj_json['Mensaje'] = "Esta verificacion ya fue cargada"
        else:
            v.user = u
            v.fecha_entrega = obj_json['Fecha']
            v.position = Geoposition(obj_json['Latitude'],
                obj_json['Longitude'])
            obj_json['Mensaje'] = "Verificacion cargada Correctamente"
            v.save()
    data = json.dumps(obj_json)
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def get_verificaciones(request):
    d = request.POST.get('departamento', '')
    departamento = Departamento.objects.get(id=d)
    queryset = Verificacion.objects.filter(iddepartamento=departamento)
    if queryset:
        data = serializers.serialize('json', queryset)
        struct = json.loads(data)
        data = json.dumps(struct)
    else:
        data = None
    return HttpResponse(data, content_type='application/json')