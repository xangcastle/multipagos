from django.db import models
from metropolitana.models import Departamento, Municipio, Barrio


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
    iddepartamento = models.ForeignKey(Departamento, null=True, blank=True)
    idmunicipio = models.ForeignKey(Municipio, null=True, blank=True)
    idbarrio = models.ForeignKey(Barrio, null=True, blank=True)

