from django.db import models
from metropolitana.models import Departamento, Municipio, Barrio, Entidad
from geoposition.fields import GeopositionField
from django.contrib.auth.models import User


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


class Cliente(Entidad):
    identificacion = models.CharField(max_length=65, null=True, blank=True)
    contrato = models.CharField(max_length=65, null=True, blank=True)
    departamento = models.ForeignKey(Departamento, null=True, blank=True,
        related_name="cartera_cliente_departamento")
    municipio = models.ForeignKey(Municipio, null=True, blank=True,
        related_name="cartera_cliente_municipio")
    barrio = models.ForeignKey(Barrio, null=True, blank=True,
        related_name="cartera_cliente_barrio")
    position = GeopositionField(null=True, blank=True)
    comentario = models.CharField(max_length=125, null=True, blank=True)
    telefonos = models.CharField(max_length=65, null=True, blank=True)

    def facturas(self):
        return Detalle.objects.filter(idcliente=self)

    def get_estado_corte(self):
        if self.facturas():
            por_pago = self.facturas().filter(pagado=False)
            for f in por_pago:
                if self.comentario == 'COBRO Y CORTE':
                    self.comentario = 'COBRO Y CORTE'
                    self.save()


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
    ESTADOS_DE_ENTREGA = (('VERIFICADA', 'VERIFICADA'),
                          ('NO VERIFICADA', 'NO VERIFICADA'),
                          ('PENDIENTE', 'PENDIENTE'),
                          ('VENCIDA', 'VENCIDA'),
                         )
    estado = models.CharField(max_length=65, null=True, blank=True,
        choices=ESTADOS_DE_ENTREGA)
    iddepartamento = models.ForeignKey(Departamento, null=True, blank=True,
        verbose_name='departamento')
    idmunicipio = models.ForeignKey('Municipio', null=True, blank=True,
        verbose_name='municipio')
    idbarrio = models.ForeignKey('Barrio', null=True, blank=True,
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
            if self.barrio and self.idmunicipio and self.iddepartamento:
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
                c, create = Cliente.objects.get_or_create(code=self.cliente,
                    contrato=self.contrato)
                c.name = self.suscriptor
                c.identificacion = self.nit
                c.telefonos = self.telefonos()
                if self.iddepartamento:
                    c.departamento = self.iddepartamento
                if self.idmunicipio:
                    c.municipio = self.idmunicipio
                if self.idbarrio:
                    c.barrio = self.idbarrio
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
        return ', '.join([self.tel_contacto, self.telefono_cliente])