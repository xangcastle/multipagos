from django.db import models
from geoposition.fields import GeopositionField
from django.contrib.auth.models import User
from metropolitana.models import get_media_url, Departamento, Municipio, \
Barrio
from datetime import datetime


def verification_data(data, ndata):
    if data == ndata:
        return 'CORRECTA'
    else:
        return 'INCORRECTA'


class Verificacion(models.Model):
    #CARGA DE BASE DE DATOS
    fecha_alta = models.DateField(null=True, blank=True)
    nombre_cliente = models.CharField(max_length=200, null=True, blank=True)
    contrato = models.IntegerField(null=True, blank=True)
    plan = models.CharField(max_length=200, null=True, blank=True,
        help_text="plan de facturacion")
    cedula = models.CharField(max_length=125, null=True, blank=True)
    servicio = models.CharField(max_length=200, null=True, blank=True)
    categoria = models.CharField(max_length=65, null=True, blank=True)
    sucursal = models.CharField(max_length=65, null=True, blank=True)
    departamento = models.CharField(max_length=125, null=True, blank=True)
    municipio = models.CharField(max_length=125, null=True, blank=True)
    barrio = models.CharField(max_length=125, null=True, blank=True)
    direccion = models.TextField(max_length=400, null=True, blank=True)
    telefono = models.CharField(max_length=125, null=True, blank=True)
    celular = models.CharField(max_length=125, null=True, blank=True)
    costo_instalacion = models.FloatField(max_length=125, null=True, blank=True)
    equipo = models.CharField(max_length=65, null=True, blank=True)
    serial = models.CharField(max_length=65, null=True, blank=True)
    mac = models.CharField(max_length=65, null=True, blank=True)
    sim = models.CharField(max_length=65, null=True, blank=True)
    solicitud = models.CharField(max_length=30, null=True, blank=True)
    #OPCIONES DE RESPUESTAS
    TIPOS_VERIFICACIONES = (
            ('CORRECTA', 'CORRECTA'),
            ('INCORRECTA', 'INCORRECTA'),
        )
    TIPOS_PROPIEDAD = (
            ('PROPIA', 'PROPIA'),
            ('FAMILIAR', 'FAMILIAR'),
            ('ALQUILADA', 'ALQUILADA'),
            ('ANTIGUEDAD', 'ANTIGUEDAD'),
        )
    ASEVERACIONES = (
            ('SI', 'SI'),
            ('NO', 'NO'),
        )
    ESTADOS = (
            ('BUENO', 'BUENO'),
            ('MALO', 'MALO'),
        )
    ###########################
    ######VERIFICACION#########
    ###########################
    direccion_ver = models.CharField(max_length=50, null=True,
        blank=True, choices=TIPOS_VERIFICACIONES,
        verbose_name="verificacion domiciliar")
    direccion_corr = models.TextField(max_length=400, null=True, blank=True,
        verbose_name="nueva direccion")
    tipo_vivienda = models.CharField(max_length=50, null=True,
        blank=True, choices=TIPOS_PROPIEDAD,
        verbose_name="tipo de vivienda")
    reside = models.CharField(max_length=24, null=True,
        blank=True, choices=ASEVERACIONES,
        verbose_name="cliente reside en la vivienda")
    #VERIFICACION Y/O ACTUALIZACION DE TELEFONOS
    telefono_ver = models.CharField(max_length=50, null=True,
        blank=True, choices=TIPOS_VERIFICACIONES,
        verbose_name="verificacion de numero de telefono")
    telefono_corr = models.CharField(max_length=125, null=True, blank=True,
        verbose_name="nueva numero de telefono")
    celular_ver = models.CharField(max_length=50, null=True,
        blank=True, choices=TIPOS_VERIFICACIONES,
        verbose_name="verificacion de numero de celular")
    celular_corr = models.CharField(max_length=125, null=True, blank=True,
        verbose_name="nuevo numero de celular")
    telefono_trabajo = models.CharField(max_length=125, null=True, blank=True,
        verbose_name="telefono del trabajo")
    #DATOS DE SERVICIO
    servicio_contratado = models.CharField(max_length=24, null=True,
        blank=True, choices=ASEVERACIONES,
        verbose_name="tiene el servicio contratado?")
    pago_instalacion = models.CharField(max_length=24, null=True,
        blank=True, choices=ASEVERACIONES,
        verbose_name="pago algun costo por instalacion del servicio?")
    costo_instalacion_corr = models.FloatField(
        max_length=125, null=True, blank=True)
    conoce_tarifa = models.CharField(max_length=24, null=True,
        blank=True, choices=ASEVERACIONES,
        verbose_name="conoce la tarifa mensual del servicio?")
    copia_contratos = models.CharField(max_length=24, null=True,
        blank=True, choices=ASEVERACIONES,
        verbose_name="posee copia de sus contratos?")
    satisfecho_servicio = models.CharField(max_length=24, null=True,
        blank=True, choices=ASEVERACIONES,
        verbose_name="esta satisfecho con el servicio contratado?")
    producto_malo = models.NullBooleanField(
        verbose_name="el producto es malo?")
    mala_atencion = models.NullBooleanField(
        verbose_name="hay constantes problemas con la atencion al cliente?")
    sin_promosiones = models.NullBooleanField(
        verbose_name="la promociones no las recibe?")
    otros = models.TextField(max_length=400, null=True, blank=True)
    #VERIFICACION DE DATOS DE EQUIPOS
    equipo_corr = models.CharField(max_length=65, null=True, blank=True)
    serial_corr = models.CharField(max_length=65, null=True, blank=True)
    mac_corr = models.CharField(max_length=65, null=True, blank=True)
    sim_corr = models.CharField(max_length=65, null=True, blank=True)
    estado_equipos = models.CharField(max_length=40, null=True,
        blank=True, choices=ESTADOS)
    #OTROS
    visita_supervisor = models.CharField(max_length=24, null=True,
        blank=True, choices=ASEVERACIONES,
        verbose_name="recibio visita de nuestro supervisor de ventas")
    comentarios = models.TextField(max_length=400, null=True, blank=True,
        verbose_name="comentarios y observaciones")
    position = GeopositionField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    fecha_asignacion = models.DateField(null=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True,
        verbose_name="fecha de ejecucion")
    fecha_vencimiento = models.DateField(null=True)
    imagen = models.FileField(upload_to=get_media_url, null=True, blank=True)
    ESTADOS_DE_ENTREGA = (('VERIFICADA', 'VERIFICADA'),
                          ('NO VERIFICADA', 'NO VERIFICADA'),
                          ('PENDIENTE', 'PENDIENTE'),
                          ('VENCIDA', 'VENCIDA'),
                         )
    estado = models.CharField(max_length=65, null=True, blank=True,
        choices=ESTADOS_DE_ENTREGA)
    iddepartamento = models.ForeignKey(Departamento, null=True, blank=True)
    idmunicipio = models.ForeignKey(Municipio, null=True, blank=True)
    idbarrio = models.ForeignKey(Barrio, null=True, blank=True)
    fecha_asignacion_user = models.DateField(null=True, blank=True)
    integrado = models.BooleanField(default=False)

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
            if self.municipio and self.iddepartamento:
                m = Municipio.objects.get(departamento=self.iddepartamento,
                    name_alt=self.municipio)
        except:
            m, created = Municipio.objects.get_or_create(
                departamento=self.iddepartamento, name=self.municipio)
        return m

    def get_barrio(self):
        b = None
        try:
            if self.barrio and self.idmunicipio and self.iddepartamento:
                b, created = Barrio.objects.get_or_create(
                departamento=self.iddepartamento,
                municipio=self.idmunicipio, name=self.barrio)
        except:
            b = Barrio.objects.filter(departamento=self.iddepartamento,
                municipio=self.idmunicipio, name=self.barrio)[0]
        return b

    def __unicode__(self):
        return self.nombre_cliente

    def get_estado(self):
        if self.fecha_vencimiento and self.fecha_vencimiento > datetime.now():
            self.estado = 'VENCIDA'
            self.save()

    def validar(self):
        self.direccion_ver = verification_data(self.direccion,
            self.direccion_corr)
        self.telefono_ver = verification_data(self.telefono,
            self.telefono_corr)
        self.celular_ver = verification_data(self.celular,
            self.celular_corr)
        if self.costo_instalacion_corr and self.costo_instalacion_corr > 0:
            self.pago_instalacion = True
        else:
            self.pago_instalacion = False

    class Meta:
        verbose_name_plural = "verificaciones"


def integrar(ps):
    message = ""
    ds = ps.order_by('departamento').distinct('departamento')
    for d in ds:
        qs = ps.filter(departamento=d.departamento)
        qs.update(iddepartamento=d.get_departamento().id)
    ms = ps.order_by('iddepartamento', 'municipio').distinct(
        'iddepartamento', 'municipio')
    for m in ms:
        qs = ps.filter(iddepartamento=m.iddepartamento,
            municipio=m.municipio)
        qs.update(idmunicipio=m.get_municipio().id)
    bs = ps.order_by('iddepartamento', 'idmunicipio', 'barrio').distinct(
        'iddepartamento', 'idmunicipio', 'barrio')
    for b in bs:
        qs = ps.filter(iddepartamento=b.iddepartamento,
            idmunicipio=b.idmunicipio, barrio=b.barrio)
        qs.update(idbarrio=b.get_barrio().id)
    ps.update(integrado=True, estado='PENDIENTE')
    message += "integrado, total de verificaciones = %s end %s departamentos" \
    % (str(ps.count()), str(ds.count()))
    return message