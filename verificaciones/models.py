from django.db import models


class Verificacion(models.Model):
    #CARGA DE BASE DE DATOS
    fecha_alta = models.DateField(null=True, blank=True)
    nombre_cliente = models.CharField(max_length=200, null=True, blank=True)
    contrato = models.IntegerField(null=True, blank=True)
    plan = models.CharField(max_length=200, null=True, blank=True,
        help_text="plan de facturacion")
    cedula = models.CharField(max_length=25, null=True, blank=True)
    servicio = models.CharField(max_length=200, null=True, blank=True)
    categoria = models.CharField(max_length=65, null=True, blank=True)
    sucursal = models.CharField(max_length=65, null=True, blank=True)
    departamento = models.CharField(max_length=125, null=True, blank=True)
    municipio = models.CharField(max_length=125, null=True, blank=True)
    barrio = models.CharField(max_length=125, null=True, blank=True)
    direccion = models.TextField(max_length=400, null=True, blank=True)
    telefono = models.CharField(max_length=25, null=True, blank=True)
    celular = models.CharField(max_length=25, null=True, blank=True)
    costo_instalacion = models.FloatField(max_length=25, null=True, blank=True)
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
    reside = models.CharField(max_length=4, null=True,
        blank=True, choices=ASEVERACIONES,
        verbose_name="cliente reside en la vivienda")
    #VERIFICACION Y/O ACTUALIZACION DE TELEFONOS
    telefono_ver = models.CharField(max_length=50, null=True,
        blank=True, choices=TIPOS_VERIFICACIONES,
        verbose_name="verificacion de numero de telefono")
    telefono_corr = models.CharField(max_length=25, null=True, blank=True,
        verbose_name="nueva numero de telefono")
    celular_ver = models.CharField(max_length=50, null=True,
        blank=True, choices=TIPOS_VERIFICACIONES,
        verbose_name="verificacion de numero de celular")
    celular_corr = models.CharField(max_length=25, null=True, blank=True,
        verbose_name="nuevo numero de celular")
    telefono_trabajo = models.CharField(max_length=25, null=True, blank=True,
        verbose_name="telefono del trabajo")
    #DATOS DE SERVICIO
    servicio_contratado = models.CharField(max_length=4, null=True,
        blank=True, choices=ASEVERACIONES,
        verbose_name="tiene el servicio contratado?")
    pago_instalacion = models.CharField(max_length=4, null=True,
        blank=True, choices=ASEVERACIONES,
        verbose_name="pago algun costo por instalacion del servicio?")
    costo_instalacion_corr = models.FloatField(
        max_length=25, null=True, blank=True)
    conoce_tarifa = models.CharField(max_length=4, null=True,
        blank=True, choices=ASEVERACIONES,
        verbose_name="conoce la tarifa mensual del servicio?")
    copia_contratos = models.CharField(max_length=4, null=True,
        blank=True, choices=ASEVERACIONES,
        verbose_name="posee copia de sus contratos?")
    satisfecho_servicio = models.CharField(max_length=4, null=True,
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
    estado_equipos = models.CharField(max_length=4, null=True,
        blank=True, choices=ESTADOS)
    #OTROS
    visita_supervisor = models.CharField(max_length=4, null=True,
        blank=True, choices=ASEVERACIONES,
        verbose_name="recibio visita de nuestro supervisor de ventas")
    comentarios = models.TextField(max_length=400, null=True, blank=True,
        verbose_name="comentarios y observaciones")

    def __unicode__(self):
        return self.nombre_cliente

    class Meta:
        verbose_name_plural = "verificaciones"