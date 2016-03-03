from django.db import models
from metropolitana.models import Departamento, Municipio, Barrio, Entidad, \
Zona
from geoposition.fields import GeopositionField
from django.contrib.auth.models import User
from django.db.models import Max
from datetime import datetime


def get_by_code(instance, code):
    model = type(instance)
    try:
        return model.objects.get(code=code)
    except:
        return instance


def get_by_name(instance, name):
    model = type(instance)
    try:
        return model.objects.get(name=name)
    except:
        return instance


def get_or_create_entidad(instance, name):
    model = type(instance)
    o, created = model.objects.get_or_create(name=name)
    o.save()
    return o


class Entrega(models.Model):
    factura = models.CharField(max_length=70, null=True, blank=True)
    contrato = models.CharField(max_length=65, null=True, blank=True)
    cliente = models.CharField(max_length=150, null=True, blank=True)
    direccion = models.TextField(null=True, blank=True)
    ciclo = models.PositiveIntegerField(null=True, blank=True)
    mes = models.PositiveIntegerField(null=True, blank=True)
    ano = models.PositiveIntegerField(null=True, blank=True)
    idbarrio = models.ForeignKey(Barrio, null=True, blank=True,
        db_column='idbarrio', verbose_name='barrio')
    iddepartamento = models.ForeignKey(Departamento, null=True, blank=True,
        db_column='iddepartamento', verbose_name='departamento')
    idmunicipio = models.ForeignKey(Municipio, null=True, blank=True,
        db_column='idmunicipio', verbose_name='municipio')
    cupon = models.PositiveIntegerField(null=True, blank=True)
    total_mes_factura = models.FloatField(null=True, blank=True)
    valor_pagar = models.FloatField(null=True, blank=True)
    numero_fiscal = models.PositiveIntegerField(null=True, blank=True)
    factura_interna = models.PositiveIntegerField(null=True, blank=True)
    telefono_contacto = models.CharField(max_length=70, null=True, blank=True)
    position = GeopositionField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    parentezco = models.CharField(max_length=75, null=True, blank=True)
    recibe = models.CharField(max_length=75, null=True, blank=True)
    ESTADOS_DE_ENTREGA = (('ENTREGADO', 'ENTREGADO'),
                          ('PENDIENTE', 'PENDIENTE'),
                          ('REZAGADO', 'REZAGADO'),
                         )
    estado = models.CharField(max_length=65, null=True, blank=True,
        choices=ESTADOS_DE_ENTREGA)
    idcliente = models.ForeignKey('Cliente', null=True, blank=True,
        db_column='idcliente', on_delete=models.SET_NULL)

    def get_cliente(self):
        c = None
        if self.contrato:
            try:
                c, create = Cliente.objects.get_or_create(
                    contrato=self.contrato)
                c.name = self.cliente
                c.departamento = self.iddepartamento
                c.municipio = self.idmunicipio
                c.barrio = self.idbarrio
                c.direccion = self.direccion
                c.save()
            except:
                c = None
        return c

    class Meta:
        managed = False
        db_table = "metropolitana_paquete"


class Cliente(Entidad):
    identificacion = models.CharField(max_length=65, null=True, blank=True)
    contrato = models.CharField(max_length=65, null=True, blank=True)
    departamento = models.ForeignKey(Departamento, null=True, blank=True,
        related_name="cartera_cliente_departamento")
    municipio = models.ForeignKey(Municipio, null=True, blank=True,
        related_name="cartera_cliente_municipio")
    barrio = models.ForeignKey(Barrio, null=True, blank=True,
        related_name="cartera_cliente_barrio")
    zona = models.ForeignKey(Zona, null=True, blank=True,
        related_name="cartera_cliente_zona")
    position = GeopositionField(null=True, blank=True)
    position_ver = models.BooleanField(default=False,
        verbose_name="con geoposicion verificada")
    comentario = models.CharField(max_length=125, null=True, blank=True)
    telefonos = models.CharField(max_length=65, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)

    def facturas(self):
        return Detalle.objects.filter(idcliente=self)

    def promesas(self):
        return PromesaPago.objects.filter(cliente=self)

    def get_estado_corte(self):
        if self.facturas():
            por_pago = self.facturas().filter(pagado=False)
            for f in por_pago:
                if f.comentario == 'COBRO Y CORTE':
                    self.comentario = 'COBRO Y CORTE'
                    self.save()

    def get_direccion(self):
        if self.facturas():
            return self.facturas().order_by('-fecha_fact')[0].direccion
        else:
            return None

    def generar_orden_corte(self):
        o, create = Corte.objects.get_or_create(cliente=self,
            estado='PENDIENTE')
        o.fecha_asignacion = datetime.now()
        if self.position:
            o.position = self.position
        o.departamento = self.departamento
        o.municipio = self.municipio
        o.barrio = self.barrio
        o.direccion = self.direccion
        o.telefonos = self.telefonos
        o.save()
        return o

    def entregas(self):
        return Entrega.objects.filter(contrato=self.contrato)

    def get_knowed_position(self):
        if self.entregas():
            entregadas = self.entregas().filter(
                estado='ENTREGADO').order_by('-fecha_entrega')
            data = []
            for e in entregadas:
                if e.position:
                    data.append(e)
            if len(data) > 0:
                self.position = data[0].position
                self.save()
            return self.position
        else:
            return None

    def get_position_verificada(self):
        if self.position:
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        self.position_ver = self.get_position_verificada()
        super(Cliente, self).save()


class Detalle(models.Model):
    cliente = models.CharField(max_length=65, null=True, blank=True)
    producto = models.CharField(max_length=65, null=True, blank=True)
    categoria = models.CharField(max_length=65, null=True, blank=True)
    contrato = models.CharField(max_length=65, null=True, blank=True)
    nit = models.CharField(max_length=65, null=True, blank=True)
    departamento = models.CharField(max_length=65, null=True, blank=True)
    localidad = models.CharField(max_length=65, null=True, blank=True)
    barr_contacto = models.CharField(max_length=125, null=True, blank=True)
    cuenta_cobro = models.CharField(max_length=65, null=True, blank=True)
    servicio = models.CharField(max_length=165, null=True, blank=True)
    factura_interna = models.CharField(max_length=65, null=True, blank=True)
    no_cupon = models.CharField(max_length=65, null=True, blank=True)
    no_fiscal = models.CharField(max_length=65, null=True, blank=True)
    saldo_pend_factura = models.FloatField(null=True, blank=True)
    ciclo = models.PositiveIntegerField(null=True, blank=True)
    ano = models.PositiveIntegerField(null=True, blank=True)
    mes = models.PositiveIntegerField(null=True, blank=True)
    fecha_fact = models.DateField(null=True, blank=True)
    fecha_venc = models.DateField(null=True, blank=True)
    tipo_mora = models.CharField(max_length=65, null=True, blank=True)
    estado_corte = models.CharField(max_length=165, null=True, blank=True)
    fecha_instalacion = models.DateField(null=True, blank=True)
    descr_plan = models.CharField(max_length=165, null=True, blank=True)
    tecnologia = models.CharField(max_length=125, null=True, blank=True)
    canal_venta = models.CharField(max_length=125, null=True, blank=True)
    ejecutivo_venta = models.CharField(max_length=125, null=True, blank=True)
    facturas_generadas = models.IntegerField(null=True, blank=True)
    facturas_pagadas = models.IntegerField(null=True, blank=True)
    tel_contacto = models.CharField(max_length=65, null=True, blank=True)
    tel_instalacion = models.CharField(max_length=65, null=True, blank=True)
    tel_contacto_cliente = models.CharField(max_length=65, null=True,
        blank=True)
    suscriptor = models.CharField(max_length=165, null=True, blank=True)
    direccion = models.TextField(max_length=400, null=True, blank=True)
    tipo_cartera = models.CharField(max_length=125, null=True, blank=True)
    recurzo_externo = models.CharField(max_length=65, null=True, blank=True)
    fecha_asignacion = models.DateField(null=True, blank=True)
    codigo = models.CharField(max_length=125, null=True, blank=True)
    comentario = models.CharField(max_length=125, null=True, blank=True)
    ESTADOS_DE_ENTREGA = (('VISITADO', 'VISITADO'),
                          ('LLAMADO', 'LLAMADO'),
                          ('CON PROMESA DE PAGO', 'CON PROMESA DE PAGO'),
                          ('PAGAGO', 'PAGADO'),
                         )
    estado = models.CharField(max_length=65, null=True, blank=True,
        choices=ESTADOS_DE_ENTREGA)
    iddepartamento = models.ForeignKey(Departamento, null=True, blank=True,
        verbose_name='departamento')
    idmunicipio = models.ForeignKey(Municipio, null=True, blank=True,
        verbose_name='municipio')
    idbarrio = models.ForeignKey(Barrio, null=True, blank=True,
        verbose_name='barrio')
    position = GeopositionField(null=True, blank=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    monto = models.FloatField(null=True, blank=True)
    idcliente = models.ForeignKey(Cliente, null=True, blank=True)
    integrado = models.NullBooleanField()
    pagado = models.NullBooleanField()

    def __unicode__(self):
        return self.cliente

    def get_departamento(self):
        d = None
        if self.departamento:
            try:
                d = Departamento.objects.get(name_alt=self.departamento)
            except:
                d, created = Departamento.objects.get_or_create(
                    name=self.departamento)
        return d

    def get_municipio(self):
        m = None
        try:
            if self.localidad and self.iddepartamento:
                m = Municipio.objects.get(departamento=self.iddepartamento,
                    name_alt=self.localidad)
        except:
            m, created = Municipio.objects.get_or_create(
                departamento=self.iddepartamento, name=self.localidad)
        return m

    def get_barrio(self):
        b = None
        try:
            if self.barr_contacto and self.idmunicipio and self.iddepartamento:
                b, created = Barrio.objects.get_or_create(
                departamento=self.iddepartamento,
                municipio=self.idmunicipio, name=self.barr_contacto)
        except:
            b = Barrio.objects.filter(departamento=self.iddepartamento,
                municipio=self.idmunicipio, name=self.barr_contacto)[0]
        return b

    def get_cliente(self):
        c = None
        if self.contrato:
            try:
                c, create = Cliente.objects.get_or_create(
                    contrato=self.contrato)
                c.code = self.cliente
                c.name = self.suscriptor
                c.identificacion = self.nit
                c.telefonos = self.telefonos()
                if self.iddepartamento:
                    c.departamento = self.iddepartamento
                if self.idmunicipio:
                    c.municipio = self.idmunicipio
                if self.idbarrio:
                    c.barrio = self.idbarrio
                c.direccion = c.get_direccion()
                c.save()
            except:
                c = None
        return c

    def integrar(self):
        self.iddepartamento = self.get_departamento()
        self.idmunicipio = self.get_municipio()
        self.idbarrio = self.get_barrio()
        self.idcliente = self.get_cliente()
        self.integrado = True
        self.save()

    def get_pagado(self):
        if self.monto and self.monto >= self.saldo_pend_factura:
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        self.pagado = self.get_pagado()
        super(Detalle, self).save()

    def telefonos(self):
        dt = []
        if self.tel_contacto:
            dt.append(self.tel_contacto)
        if self.tel_contacto_cliente:
            dt.append(self.tel_contacto_cliente)
        return ', '.join(dt)


class Corte(models.Model):
    cliente = models.ForeignKey(Cliente)
    fecha_asignacion = models.DateTimeField(null=True)
    user_solicita = models.ForeignKey(User, null=True,
        related_name='usuario_que_solicita')
    user = models.ForeignKey(User, null=True)
    fecha = models.DateTimeField(null=True)
    numero = models.IntegerField(null=True)
    position = GeopositionField(null=True)
    departamento = models.ForeignKey(Departamento, null=True)
    municipio = models.ForeignKey(Municipio, null=True)
    barrio = models.ForeignKey(Barrio, null=True)
    comentario = models.CharField(max_length=125, null=True, blank=True)
    telefonos = models.CharField(max_length=65, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    ESTADOS_DE_CORTE = (
        ('PENDIENTE', 'PENDIENTE'),
        ('CORTADO', 'CORTADO'),
        ('ANULADO', 'ANULADO'),
        )
    estado = models.CharField(max_length=50, choices=ESTADOS_DE_CORTE,
        default='PENDIENTE')

    def __unicode__(self):
        return 'orde de corte # %s' % self.numero

    def get_numero(self):
        queryset = type(self).objects.all()
        if queryset.count() > 0:
            mayor = queryset.aggregate(Max('numero'))['numero__max']
            return (mayor + 1)
        else:
            return 1

    def save(self, *args, **kwargs):
        if not self.numero:
            self.numero = self.get_numero()
        super(Corte, self).save()

    class Meta:
        verbose_name = 'orden'
        verbose_name_plural = 'ordenes de corte'

    def to_json(self):
        obj = {}
        obj['pk'] = self.id
        obj['fecha_asignacion'] = str(self.fecha_asignacion)
        obj['numero'] = str(self.numero)
        obj['cliente_pk'] = str(self.cliente.id)
        obj['cliente_nombre'] = str(self.cliente.name)
        obj['departamento'] = str(self.departamento.name)
        obj['municipio'] = str(self.municipio.name)
        obj['barrio'] = str(self.barrio.name)
        obj['direccion'] = str(self.direccion)
        obj['telefonos'] = str(self.telefonos)
        return obj


class PromesaPago(models.Model):

    cliente = models.ForeignKey(Cliente)
    corte = models.ForeignKey(Corte)
    user = models.ForeignKey(User)
    fecha_promesa = models.DateTimeField(auto_now_add=True)
    fecha_pago = models.DateField()

    def __unicode__(self):
        return '%s %s' % (self.cliente.name, str(self.fecha_pago))


class Gestion(models.Model):
    detalle = models.ForeignKey(Detalle)
    user = models.ForeignKey(User)
    fecha = models.DateTimeField(auto_now_add=True)
    tipo_gestion = models.ForeignKey('TipoGestion', null=True)


class TipoGestion(models.Model):
    signo = models.CharField(max_length=4)
    descripcion = models.CharField(max_length=255)
    RESULTADOS = (
    ('RECLAMO', 'RECLAMO'),
    ('PROMESA DE PAGO', 'PROMESA DE PAGO'),
    ('PROBLEMAS ECONOMICOS', 'PROBLEMAS ECONOMICOS'),
    ('CLIENTE NO CONTACTADO', 'CLIENTE NO CONTACTADO'),
    ('NO EXISTEN PUNTOS DE PAGO', 'NO EXISTEN PUNTOS DE PAGO'),
        )
    resultado = models.CharField(max_length=60,
        choices=RESULTADOS)

    def __unicode__(self):
        return '%s %s' % (self.signo, self.descripcion)