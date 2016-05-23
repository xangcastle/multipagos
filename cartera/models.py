from django.db import models
from metropolitana.models import Departamento, Municipio, Barrio, Entidad, \
Zona, get_code, get_zona
from geoposition.fields import GeopositionField
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import datetime


def devolver_mayor(a, b):
    if a and not b:
        return a
    else:
        return b
    if len(a) > len(b):
        return a
    else:
        return b


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
        related_name="cartera_cliente_departamento", on_delete=models.SET_NULL)
    municipio = models.ForeignKey(Municipio, null=True, blank=True,
        related_name="cartera_cliente_municipio", on_delete=models.SET_NULL)
    barrio = models.ForeignKey(Barrio, null=True, blank=True,
        related_name="cartera_cliente_barrio", on_delete=models.SET_NULL)
    zona = models.ForeignKey(Zona, null=True, blank=True,
        related_name="cartera_cliente_zona", on_delete=models.SET_NULL)
    position = GeopositionField(null=True, blank=True)
    position_ver = models.BooleanField(default=False,
        verbose_name="con geoposicion verificada")
    comentario = models.CharField(max_length=125, null=True, blank=True)
    telefonos = models.CharField(max_length=265, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    tipo_mora = models.ForeignKey('TipoMora', null=True, blank=True,
        on_delete=models.SET_NULL)
    saldo_total = models.FloatField(null=True, blank=True)
    ciclo = models.PositiveIntegerField(null=True, blank=True)
    estado_corte = models.CharField(max_length=165, null=True, blank=True)
    fecha_instalacion = models.DateField(null=True, blank=True)
    descr_plan = models.CharField(max_length=165, null=True, blank=True)
    tecnologia = models.CharField(max_length=125, null=True, blank=True)
    canal_venta = models.CharField(max_length=125, null=True, blank=True)
    ejecutivo_venta = models.CharField(max_length=125, null=True, blank=True)
    facturas_generadas = models.IntegerField(null=True, blank=True)
    facturas_pagadas = models.IntegerField(null=True, blank=True)
    has_pend = models.BooleanField(default=False,
        verbose_name="con gestiones pendientes")

    def facturas(self):
        return Factura.objects.filter(cliente=self, saldo__gt=0.0)

    def gestiones(self):
        return Gestion.objects.filter(cliente=self).exclude(
            estado='PENDIENTE').order_by("fecha_gestion")

    def get_estado_mora(self):
        if self.facturas():
            for f in self.facturas():
                self.tipo_mora = devolver_mora_mayor(self.tipo_mora,
                    f.idtipo_mora)
            self.save()

    def get_saldo(self):
        if self.facturas():
            return self.facturas().aggregate(
                Sum('saldo'))['saldo__sum']
        else:
            return 0.0

    def add_saldo(self, monto):
        if self.saldo_total:
            self.saldo_total += monto
        else:
            self.saldo_total = monto

    def actualizar_saldo(self):
        self.saldo_total = self.get_saldo()
        self.save()

    def get_direccion(self):
        if self.facturas():
            return self.facturas().order_by('-fecha_fact')[0].direccion
        else:
            return None

    def generar_gestion(self, tipo, user=None):
        o, create = Gestion.objects.get_or_create(cliente=self,
            estado='PENDIENTE', tipo_gestion=tipo)
        o.fecha_asignacion = datetime.now()
        if self.departamento:
            o.departamento = self.departamento
        if self.municipio:
            o.municipio = self.municipio
        if self.barrio:
            o.barrio = self.barrio
        if not self.zona and self.barrio:
            self.zona = get_zona(self.barrio)
            self.save()
        o.zona = self.zona
        if self.position:
            o.position = self.position
        if not self.ciclo:
            self.ciclo = self.get_ciclo()
            self.save()
        o.ciclo = self.ciclo
        o.contrato = self.contrato
        o.comentario = self.comentario
        o.tipo_mora = self.tipo_mora
        o.descr_plan = self.descr_plan
        o.user = user
        o.save()
        return o

    def get_knowed_position(self):
        if self.facturas():
            entregadas = self.facturas().filter(
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

    def get_comentario(self):
        if self.facturas():
            return self.facturas().order_by('-fecha_asignacion')[0].comentario
        else:
            return ""

    def get_ciclo(self):
        if self.facturas():
            return self.facturas().order_by('-fecha_asignacion')[0].ciclo
        else:
            return None

    def get_position_verificada(self):
        if self.position:
            return True
        else:
            return False

    def __unicode__(self):
        return ' '.join([
            str(self.contrato), self.name])

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = get_code(self, 6)
        self.position_ver = self.get_position_verificada()
        super(Cliente, self).save()


class import_model(models.Model):
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
    factura = models.CharField(max_length=65, null=True, blank=True)
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
    fecha_fin = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return self.suscriptor

    def __getitem__(self, fieldname):
        try:
            return getattr(self, fieldname)
        except:
            return None

    def __setitem__(self, key, value):
        try:
            setattr(self, key, value)
            return True
        except:
            return False

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
            if self.localidad:
                m = Municipio.objects.get(departamento=self.get_departamento(),
                    name_alt=self.localidad)
        except:
            m, created = Municipio.objects.get_or_create(
                departamento=self.get_departamento(), name=self.localidad)
        return m

    def get_barrio(self):
        b = None
        try:
            if self.barr_contacto:
                b, created = Barrio.objects.get_or_create(
                departamento=self.get_departamento(),
                municipio=self.get_municipio(), name=self.barr_contacto)
        except:
            b = Barrio.objects.filter(departamento=self.get_departamento(),
                municipio=self.get_municipio(), name=self.barr_contacto)[0]
        return b

    def get_mora(self):
        m = None
        if self.tipo_mora:
            m, created = TipoMora.objects.get_or_create(name=self.tipo_mora)
        else:
            m, created = TipoMora.objects.get_or_create(name='AL_DIA')
        return m

    def telefonos(self):
        dt = []
        if self.tel_contacto:
            dt.append(self.tel_contacto)
        if self.tel_contacto_cliente:
            dt.append(self.tel_contacto_cliente)
        return ', '.join(dt)

    def get_cliente(self):
        c, create = Cliente.objects.get_or_create(
            contrato=self.contrato)
        c.code = devolver_mayor(self.cliente, c.code)
        c.name = devolver_mayor(self.suscriptor, c.name)
        c.identificacion = devolver_mayor(self.nit, c.identificacion)
        c.telefonos = devolver_mayor(self.telefonos(), c.telefonos)
        if not c.direccion:
            c.direccion = self.direccion
        if not c.ciclo:
            c.ciclo = self.ciclo
        if not c.comentario:
            c.comentario = self.comentario
        c.saldo_total = c.get_saldo()
        if not c.departamento:
            c.departamento = self.get_departamento()
        if not c.municipio:
            c.municipio = self.get_municipio()
        if not c.barrio:
            c.barrio = self.get_barrio()
        if not c.zona:
            c.zona = get_zona(self.get_barrio())
        if not c.tipo_mora:
            c.tipo_mora = self.get_mora()
        c.estado_corte = self.estado_corte
        c.fecha_instalacion = devolver_mayor(c.fecha_instalacion,
            self.fecha_instalacion)
        c.descr_plan = devolver_mayor(self.descr_plan, c.descr_plan)
        c.tecnologia = devolver_mayor(self.tecnologia, c.tecnologia)
        c.canal_venta = devolver_mayor(self.canal_venta, c.canal_venta)
        c.ejecutivo_venta = devolver_mayor(self.ejecutivo_venta,
            c.ejecutivo_venta)
        c.facturas_generadas = self.facturas_generadas
        c.facturas_pagadas = self.facturas_pagadas
        c.save()
        if self.comentario == "COBRO":
            c.generar_gestion(TipoGestion.objects.get(code='0002'))
        return c

    def get_factura(self):
        if self.no_cupon:
            f, created = Factura.objects.get_or_create(no_cupon=self.no_cupon)
        if not self.no_cupon and self.factura_interna:
            f, created = Factura.objects.get_or_create(
                factura_interna=self.factura_interna)
        f.cliente = self.get_cliente()
        f.tipo_mora = self.get_mora()
        if not self.factura:
            f.factura = self.factura
        if not self.factura_interna:
            f.factura_interna = self.factura_interna
        if not self.no_fiscal:
            f.no_fiscal = self.no_fiscal
        f.saldo_pend_factura = self.saldo_pend_factura
        if not self.ciclo:
            f.ciclo = self.ciclo
        if not self.mes:
            f.mes = self.mes
        if not self.ano:
            f.ano = self.ano
        if self.fecha_fact:
            f.fecha_fact = self.fecha_fact
        if self.fecha_venc:
            f.fecha_venc = self.fecha_venc
        f.saldo = self.saldo_pend_factura
        f.save()
        f.cliente.actualizar_saldo()
        return f

    def integrar(self):
        self.get_factura()
        self.delete()

    class Meta:
        verbose_name = "registro"
        verbose_name_plural = "importacion de datos"


class Factura(models.Model):
    cliente = models.ForeignKey(Cliente, null=True, blank=True,
        on_delete=models.SET_NULL)
    tipo_mora = models.ForeignKey('TipoMora', null=True, blank=True)
    factura = models.CharField(max_length=65, null=True, blank=True)
    factura_interna = models.CharField(max_length=65, null=True, blank=True)
    no_cupon = models.CharField(max_length=65, null=True, blank=True)
    no_fiscal = models.CharField(max_length=65, null=True, blank=True)
    saldo_pend_factura = models.FloatField(null=True, blank=True)
    ciclo = models.PositiveIntegerField(null=True, blank=True)
    ano = models.PositiveIntegerField(null=True, blank=True)
    mes = models.PositiveIntegerField(null=True, blank=True)
    fecha_fact = models.DateField(null=True, blank=True)
    fecha_venc = models.DateField(null=True, blank=True)
    gestionada = models.BooleanField(default=False)
    monto_abonado = models.FloatField(default=0.0)
    saldo = models.FloatField(null=True)
    fecha_pago = models.DateTimeField(null=True)
    user = models.ForeignKey(User, null=True)

    def get_saldo(self):
        if self.saldo_pend_factura and self.monto_abonado:
            return self.saldo_pend_factura - self.monto_abonado
        else:
            return self.saldo_pend_factura

    def save(self, *args, **kwargs):
        self.saldo = self.get_saldo()
        super(Factura, self).save()

    class Meta:
        verbose_name_plural = "detalle de mora"
        verbose_name = "factura"


class Gestion(models.Model):
    cliente = models.ForeignKey(Cliente)
    departamento = models.ForeignKey(Departamento, null=True, blank=True)
    municipio = models.ForeignKey(Municipio, null=True, blank=True)
    barrio = models.ForeignKey(Barrio, null=True, blank=True)
    ciclo = models.PositiveIntegerField(null=True, blank=True)
    zona = models.ForeignKey(Zona, null=True, blank=True)
    position = GeopositionField(null=True, blank=True)
    user = models.ForeignKey(User, null=True)
    fecha_asignacion = models.DateTimeField(null=True)
    fecha_vencimiento = models.DateTimeField(null=True)
    fecha_gestion = models.DateTimeField(null=True)
    tipo_gestion = models.ForeignKey('TipoGestion', null=True)
    tipo_resultado = models.ForeignKey('TipoResultado', null=True)
    fecha_promesa = models.DateField(null=True,
        verbose_name="fecha de promesa de pago")
    observaciones = models.CharField(max_length=255, null=True)
    contrato = models.CharField(max_length=65, null=True, blank=True)
    comentario = models.CharField(max_length=125, null=True, blank=True)
    tipo_mora = models.ForeignKey('TipoMora', null=True, blank=True,
            on_delete=models.SET_NULL)
    descr_plan = models.CharField(max_length=165, null=True, blank=True)
    ESTADOS_GESTION = (
        ('PENDIENTE', 'PENDIENTE'),
        ('REALIZADO', 'REALIZADO'),
        ('VENCIDO', 'VENCIDO'),
        )
    estado = models.CharField(max_length=65, default='PENDIENTE',
        choices=ESTADOS_GESTION)

    def __unicode__(self):
        return str(self.tipo_gestion) + ' ' + self.cliente.name

    def to_json(self):
        obj = {}
        obj['pk'] = self.id
        obj['fecha_asignacion'] = str(self.fecha_asignacion)
        obj['cliente_pk'] = str(self.cliente.id)
        obj['cliente_nombre'] = self.cliente.name
        obj['departamento'] = self.cliente.departamento.name
        obj['municipio'] = self.cliente.municipio.name
        obj['barrio'] = self.cliente.barrio.name
        obj['direccion'] = self.cliente.direccion
        obj['telefonos'] = self.cliente.telefonos
        return obj

    class Meta:
        verbose_name_plural = "gestiones"

    def aplicar(self):
        if self.cliente:
            self.cliente.get_knowed_position()
            self.cliente.comentario = self.tipo_resultado.descripcion
            self.cliente.save()


class TipoGestion(Entidad):

    class Meta:
        verbose_name = "tipo de gestion"
        verbose_name_plural = "tipos de gestiones"


class TipoResultado(models.Model):
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


class TipoMora(models.Model):
    name = models.CharField(max_length=125, null=True,
        verbose_name="descripcion")
    dias = models.IntegerField(null=True,
        verbose_name="cantidad de dias en mora")

    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return ''

    class Meta:
        ordering = ['dias', ]


class AsignacionCliente(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    cliente = models.ForeignKey(Cliente, null=True, on_delete=models.SET_NULL)
    tipo_gestion = models.ForeignKey(TipoGestion, null=True,
        on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.cliente.name + ' - ' + self.user.username

    class Meta:
        unique_together = ('user', 'cliente', 'tipo_gestion')
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios asignados'


class RebajaCartera(models.Model):
    no_cupon = models.CharField(max_length=65, null=True)
    fecha_pago = models.DateField(null=True)
    abono = models.FloatField(null=True)

    class Meta:
        verbose_name = "registro"
        verbose_name_plural = "importacion de rebajas de cartera"

    def integrar(self):
        try:
            f = Factura.objects.get(no_cupon=self.no_cupon)
            f.gestionada = True
            f.monto_abonado = self.abono
            f.fecha_pago = self.fecha_pago
            f.saldo = f.saldo_pend_factura - f.monto_abonado
            f.save()
            self.delete()
        except:
            if not self.no_cupon:
                self.delete()


class NewGestion(models.Model):
    contrato_cliente = models.CharField(max_length=65, null=True, blank=True)
    user_id = models.CharField(max_length=65, null=True, blank=True)
    gestion_code = models.CharField(max_length=65, null=True, blank=True)
    fecha_asignacion = models.DateField(null=True)
    fecha_vence = models.DateField(null=True)

    def get_cliente(self):
        try:
            c = Cliente.objects.get(contrato=self.contrato_cliente)
        except:
            c = None
        return c

    def get_gestion(self):
        try:
            c = TipoGestion.objects.get(code=self.gestion_code)
        except:
            c = None
        return c

    def get_user(self):
        try:
            c = User.objects.get(id=int(self.user_id))
        except:
            c = None
        return c

    def integrar(self):
        c = self.get_cliente()
        tg = self.get_gestion()
        u = self.get_user()
        if c and tg and u:
            g = c.generar_gestion(tg)
            g.user = u
            g.fecha_asignacion = self.fecha_asignacion
            g.fecha_vencimiento = self.fecha_vence
            g.save()
            self.delete()

    def __unicode__(self):
        return ' - '.join([self.contrato_cliente, self.gestion_code])

    def save(self, *args, **kwargs):
        super(NewGestion, self).save()
        self.integrar()


def integrar_importacion(ps):
    message = ""
    ds = ps.order_by('departamento').distinct('departamento')
    clientes = []
    for d in ds:
        depto = d.get_departamento()
        queryset = ps.filter(departamento=d.departamento)
        ms = queryset.order_by('localidad').distinct('localidad')
        for m in ms:
            mcipio = m.get_municipio()
            queryset = ps.filter(departamento=d.departamento,
                localidad=d.localidad)
            bs = queryset.order_by('barr_contacto').distinct('barr_contacto')
            for b in bs:
                brrio = b.get_barrio()
                queryset = ps.filter(departamento=d.departamento,
                    localidad=d.localidad, barr_contacto=d.barr_contacto)
                cs = queryset.order_by('contrato').distinct('contrato')
                for c in cs:
                    cl, created = Cliente.objects.get_or_create(
                        contrato=c.contrato)
                    cl.name = c.suscriptor
                    cl.departamento = depto
                    cl.municipio = mcipio
                    cl.barrio = brrio
                    cl.save()
                    clientes.append(cl)
    print(clientes)
    message += "integrado, total de facturas = %s end %s departamentos" \
    % (str(ps.count()), str(ds.count()))
    return message


def devolver_mora_mayor(m1, m2):
    if not m1 and not m2:
        return None
    if m1 and not m2:
        return m1
    if m2 and not m1:
        return m2
    if m1.dias > m2.dias:
        return m1
    else:
        return m2