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
from cartera.models import Detalle, Cliente


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
    obj_json['Pk'] = request.POST.get('Pk', '')
    obj_json['IdUsuario'] = request.POST.get('IdUsuario', '')
    obj_json['Fecha'] = str(request.POST.get('Fecha', ''))
    obj_json['Latitude'] = request.POST.get('Latitude', '')
    obj_json['Longitude'] = request.POST.get('Longitude', '')
    obj_json['Estado'] = request.POST.get('Estado', '')

    obj_json['direccion_corr'] = request.POST.get('direccion_corr', None)
    obj_json['tipo_vivienda'] = request.POST.get('tipo_vivienda', None)
    obj_json['reside'] = request.POST.get('reside', None)
    obj_json['telefono_corr'] = request.POST.get('telefono_corr', None)
    obj_json['celular_corr'] = request.POST.get('celular_corr', None)
    obj_json['telefono_trabajo'] = request.POST.get('telefono_trabajo', None)
    obj_json['servicio_contratado'] = request.POST.get('servicio_contratado', None)
    obj_json['pago_instalacion'] = request.POST.get('pago_instalacion', None)
    obj_json['costo_instalacion_corr'] = request.POST.get('costo_instalacion_corr', None)
    obj_json['conoce_tarifa'] = request.POST.get('conoce_tarifa', None)
    obj_json['copia_contratos'] = request.POST.get('copia_contratos', None)
    obj_json['satisfecho_servicio'] = request.POST.get('satisfecho_servicio', None)
    obj_json['producto_malo'] = request.POST.get('producto_malo', None)
    obj_json['mala_atencion'] = request.POST.get('mala_atencion', None)
    obj_json['sin_promosiones'] = request.POST.get('sin_promosiones', None)
    obj_json['equipo_corr'] = request.POST.get('equipo_corr', None)
    obj_json['serial_corr'] = request.POST.get('serial_corr', None)
    obj_json['mac_corr'] = request.POST.get('mac_corr', None)
    obj_json['sim_corr'] = request.POST.get('sim_corr', None)
    obj_json['estado_equipos'] = request.POST.get('estado_equipos', None)
    obj_json['visita_supervisor'] = request.POST.get('visita_supervisor', None)
    obj_json['comentarios'] = request.POST.get('comentarios', None)

    obj_json['Mensaje'] = ''
    try:
        u = User.objects.get(id=int(obj_json['IdUsuario']))
    except:
        u = None
    try:
        v = Verificacion.objects.get(id=int(obj_json['Pk']))
    except:
        v = None
    if v:
        v.user = u
        v.fecha_entrega = obj_json['Fecha']
        v.position = Geoposition(obj_json['Latitude'],
            obj_json['Longitude'])
        v.estado = obj_json['Estado']
        v.direccion_corr = obj_json['direccion_corr']
        v.tipo_vivienda = obj_json['tipo_vivienda']
        v.reside = obj_json['reside']
        v.telefono_corr = obj_json['telefono_corr']
        v.celular_corr = obj_json['celular_corr']
        v.telefono_trabajo = obj_json['telefono_trabajo']
        v.servicio_contratado = obj_json['servicio_contratado']
        v.pago_instalacion = obj_json['pago_instalacion']
        v.costo_instalacion_corr = obj_json['costo_instalacion_corr']
        v.conoce_tarifa = obj_json['conoce_tarifa']
        v.copia_contratos = obj_json['copia_contratos']
        v.satisfecho_servicio = obj_json['satisfecho_servicio']
        v.producto_malo = obj_json['producto_malo']
        v.mala_atencion = obj_json['mala_atencion']
        v.sin_promosiones = obj_json['sin_promosiones']
        v.equipo_corr = obj_json['equipo_corr']
        v.serial_corr = obj_json['serial_corr']
        v.mac_corr = obj_json['mac_corr']
        v.sim_corr = obj_json['sim_corr']
        v.estado_equipos = obj_json['estado_equipos']
        v.visita_supervisor = obj_json['visita_supervisor']
        v.comentarios = obj_json['comentarios']

        obj_json['Mensaje'] = "Verificacion cargada Correctamente"
        v.save()
    data = json.dumps(obj_json)
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def get_verificaciones(request):
    d = request.POST.get('departamento', '')
    departamento = Departamento.objects.get(id=d)
    queryset = Verificacion.objects.filter(iddepartamento=departamento).exclude(
        estado='VENCIDA')
    if queryset:
        data = serializers.serialize('json', queryset)
        struct = json.loads(data)
        data = json.dumps(struct)
    else:
        data = None
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def get_cartera(request):
    data = []
    d = request.POST.get('departamento', '')
    departamento = Departamento.objects.get(id=d)
    queryset = Cliente.objects.filter(departamento=departamento)
    for c in queryset:
        obj_json = {}
        obj_json['code'] = c.code
        obj_json['name'] = c.name
        obj_json['identificacion'] = c.identificacion
        obj_json['departamento'] = c.departamento.name
        obj_json['municipio'] = c.municipio.name
        obj_json['barrio'] = c.barrio.name
        facs = []
        for f in c.facturas():
            fac_json = {}
            fac_json['Pk'] = f.id
            fac_json['factura_interna'] = f.factura_interna
            fac_json['no_cupon'] = f.no_cupon
            fac_json['saldo_pend_factura'] = f.saldo_pend_factura
            fac_json['fecha_fact'] = f.fecha_fact
            fac_json['fecha_venc'] = f.fecha_venc
            fac_json['tipo_mora'] = f.tipo_mora
            facs.append(fac_json)
        obj_json['facturas'] = facs
        data.append(obj_json)
    struct = json.loads(data)
    data = json.dumps(struct)
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def get_detalle(request):
    obj_json = {'Mensaje': ''}
    try:
        d = Detalle.objects.get(id=int(request.POST.get('Pk')))
    except:
        d = None
    try:
        u = User.objects.get(id=int(request.POST.get('Usuario')))
    except:
        pass
    if d:
        d.position = Geoposition(request.POST.get('Latitude', ''),
                    request.POST.get('Longitude', ''))
        d.user = u
        d.fecha_entrega = request.POST.get('Fecha', '')
        d.monto = request.POST.get('Monto', '')
        d.save()
        obj_json['Mensaje'] = 'Registro grabado con exito'
    data = json.dumps(obj_json)
    return HttpResponse(data, content_type='application/json')