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
from cartera.models import Detalle, Cliente, Corte, Gestion, TipoGestion


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
    usuario = User.objects.get(id=int(request.POST.get('usuario', '')))
    queryset = Verificacion.objects.filter(user=usuario, estado='PENDIENTE')
    if queryset:
        data = serializers.serialize('json', queryset)
        struct = json.loads(data)
        data = json.dumps(struct)
    else:
        data = None
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def get_cartera(request):
    usuario = User.objects.get(id=int(request.POST.get('usuario', '')))
    data = []
    queryset = cartera_user(usuario)
    for c in queryset:
        obj_json = {}
        obj_json['code'] = c.id
        obj_json['name'] = c.name
        obj_json['contrato'] = c.contrato
        obj_json['identificacion'] = c.identificacion
        obj_json['departamento'] = c.departamento.name
        obj_json['municipio'] = c.municipio.name
        obj_json['barrio'] = c.barrio.name
        obj_json['direccion'] = c.direccion
        obj_json['telefonos'] = c.telefonos
        obj_json['comentario'] = c.comentario
        facs = []
        pmsas = []
        for f in c.facturas():
            fac_json = {}
            fac_json['Pk'] = f.id
            fac_json['factura_interna'] = f.factura_interna
            fac_json['no_cupon'] = f.no_cupon
            fac_json['saldo_pend_factura'] = f.saldo_pend_factura
            fac_json['fecha_fact'] = str(f.fecha_fact)
            fac_json['fecha_venc'] = str(f.fecha_venc)
            fac_json['tipo_mora'] = f.tipo_mora
            facs.append(fac_json)
        obj_json['facturas'] = facs
        for p in c.promesas():
            prm_json = {}
            prm_json['Pk'] = p.id
            prm_json['user'] = p.user.username
            prm_json['fecha_promesa'] = str(p.fecha_promesa)
            prm_json['fecha_pago'] = str(p.fecha_pago)
            pmsas.append(prm_json)
        obj_json['promesas'] = pmsas
        data.append(obj_json)
    data = json.dumps(data)
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
        d.estado = 'PAGADO'
        d.save()
        obj_json['Mensaje'] = 'Registro grabado con exito'
    data = json.dumps(obj_json)
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def get_cortes(request):
    data = []
    usuario = User.objects.get(id=int(request.POST.get('usuario', '')))
    queryset = Corte.objects.filter(user=usuario, estado='PENDIENTE')
    if queryset:
        for c in queryset:
            data.append(c.to_json())
        data = json.dumps(data)
    else:
        data = None
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def put_corte(request):
    data = {'Mensaje': ''}
    c = request.POST.get('Cliente', '')
    u = request.POST.get('Usuario', '')
    cliente = Cliente.objects.get(id=int(c))
    user = User.objects.get(id=int(u))
    orden = cliente.generar_orden_corte()
    orden.user_solicita = user
    orden.fecha = request.POST.get('Fecha', '')
    orden.save()
    data['Numero'] = orden.numero
    data['Mensaje'] = 'orden generada con exito'
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def get_corte(request):
    o = Corte.objects.get(id=int(request.POST.get('Pk', '')))
    o.fecha = request.POST.get('Fecha', '')
    o.user = User.objects.get(id=int(request.POST.get('Usuario', '')))
    o.position = Geoposition(request.POST.get('Latitude', ''),
                    request.POST.get('Longitude', ''))
    o.estado = 'CORTADO'
    o.save()
    data = {'Mensaje': 'orden grabada con exito'}
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def get_gestion(request):
    obj_json = {'Mensaje': ''}
    obj_json['contrato'] = request.POST.get('contrato', '')
    obj_json['user'] = request.POST.get('user', '')
    obj_json['tipo_gestion'] = request.POST.get('tipo_gestion', '')
    obj_json['fecha'] = request.POST.get('fecha', '')
    obj_json['fecha_promesa'] = request.POST.get('fecha_promesa', '')
    obj_json['observaciones'] = request.POST.get('observaciones', '')
    try:
        tg = TipoGestion.objects.get(signo=obj_json['tipo_gestion'])
    except:
        tg = None
    try:
        c = Cliente.objects.get(contrato=obj_json['contrato'])
    except:
        c = None
    try:
        u = TipoGestion.objects.get(id=obj_json['user'])
    except:
        u = None
    if tg and c and u:
        g = Gestion(cliente=c, user=u, tipo_gestion=tg,
            observaciones=obj_json['observaciones'],
            fecha=obj_json['fecha'])
        g.save()
        obj_json['Mensaje'] = "gestion guardada con exito"
    data = json.dumps(obj_json)
    return HttpResponse(data, content_type='application/json')


def cartera_user(user):
    isc = Detalle.objects.filter(estado='PENDIENTE', user=user
    ).order_by('idcliente').values_list(
        'idcliente', flat=True)
    cs = Cliente.objects.filter(id__in=isc)
    return cs