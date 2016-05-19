# -*- coding: latin-1 -*-
from django.db import models
from django.db.models import Max, Min
import os
import shutil
from django.conf import settings
import subprocess
from geoposition.fields import GeopositionField
from django.contrib.auth.models import User
import time
from django.forms.models import model_to_dict


def smart_text(text):
    try:
        return text
    except:
        return '~'


def get_code(entidad, length=4):
        model = type(entidad)
        code = ''
        sets = model.objects.filter(code__isnull=False)
        if sets:
            maxi = str(sets.aggregate(Max('code'))['code__max'])
            if maxi:
                consecutivo = list(range(1, int(maxi)))
                ocupados = list(sets.values_list('code',
                flat=True))
                n = 0
                for l in ocupados:
                    ocupados[n] = int(str(l))
                    n += 1
                disponibles = list(set(consecutivo) - set(ocupados))
                if len(disponibles) > 0:
                    code = min(disponibles)
                else:
                    code = max(ocupados) + 1
        else:
            code = 1
        return str(code).zfill(length)


def get_code_cliente(entidad):
        model = type(entidad)
        code = ''
        sets = model.objects.filter(code__isnull=False)
        if sets:
            maxi = str(sets.aggregate(Max('code'))['code__max'])
            if maxi:
                consecutivo = list(range(1, int(maxi)))
                ocupados = list(sets.values_list('code',
                flat=True))
                n = 0
                for l in ocupados:
                    ocupados[n] = int(str(l))
                    n += 1
                disponibles = list(set(consecutivo) - set(ocupados))
                if len(disponibles) > 0:
                    code = min(disponibles)
                else:
                    code = max(ocupados) + 1
        return str(code).zfill(8)


def get_media_url(model, filename):
    clase = model.__class__.__name__
    code = str(model.id)
    return '%s/%s/%s' % (clase, code, filename)


def get_servicio(ciclo):
    carpeta_ciclo = ''
    if ciclo in (33, 88):
        carpeta_ciclo = 'internet'
    if ciclo in (55, 66):
        carpeta_ciclo = 'lineas_fijas'
    if ciclo in (65, 51):
        carpeta_ciclo = 'lineas_moviles'
    if ciclo in (10,):
        carpeta_ciclo = 'datos'
    if ciclo in (1, 77, 11, 76):
        carpeta_ciclo = 'TV'
    return carpeta_ciclo


def get_ruta(paquete):
    carpata_madre = str(paquete.ano)[2:4] + str(paquete.mes).zfill(2) \
        + str(paquete.ciclo).zfill(2)
    ruta = os.path.join('POD', carpata_madre, 'Factura PDF')
    return ruta


def generar_ruta_comprobante(paquete, filename):
        extension = os.path.splitext(filename)[1][1:]
        nombre = paquete.name_file()
        nombre_archivo = '{}.{}'.format(nombre, extension)
        ruta = os.path.join(get_ruta(paquete), nombre_archivo)
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, ruta))
        except:
            pass
        return ruta


class base(models.Model):

    def __iter__(self):
        for field_name in self._meta.get_all_field_names():
            try:
                value = getattr(self, field_name)
            except:
                value = None
            yield (field_name, value)

    class Meta:
        abstract = True


class base_entidad(base):
    code = models.CharField(max_length=25, null=True, blank=True,
        verbose_name="codigo")
    name = models.CharField(max_length=100, verbose_name="nombre")

    class Meta:
        abstract = True


class Entidad(base_entidad):
    activo = models.BooleanField(default=True)

    def __unicode__(self):
        if self.code and self.name:
            return str(self.code) + " " + self.name
        elif self.name:
            return self.name
        elif self.code:
            return str(self.code)
        else:
            return ''

    @staticmethod
    def autocomplete_search_fields():
        return ("code__iexact", "name__icontains",)

    def save(self, *args, **kwargs):
        if self.code is None or self.code == '':
            self.code = get_code(self)
        super(Entidad, self).save()

    class Meta:
        abstract = True
        ordering = ['name']


class Paquete(base):
    archivo = models.CharField(max_length=100, null=True, blank=True,
    verbose_name="archivo segmentado")
    consecutivo = models.PositiveIntegerField(null=True, blank=True)
    contrato = models.PositiveIntegerField(null=True, blank=True)
    factura = models.CharField(max_length=70, null=True, blank=True)
    ciclo = models.PositiveIntegerField(null=True, blank=True)
    mes = models.PositiveIntegerField(null=True, blank=True)
    ano = models.PositiveIntegerField(null=True, blank=True)
    cliente = models.CharField(max_length=150, null=True, blank=True)
    direccion = models.TextField(max_length=250, null=True, blank=True)
    barrio = models.CharField(max_length=150, null=True, blank=True)
    municipio = models.CharField(max_length=150, null=True, blank=True)
    departamento = models.CharField(max_length=150, null=True, blank=True)
    distribuidor = models.CharField(max_length=150, null=True, blank=True)
    ruta = models.CharField(max_length=25, null=True, blank=True)
    zona = models.PositiveIntegerField(null=True, blank=True)
    telefono = models.CharField(max_length=50, null=True, blank=True)
    segmento = models.CharField(max_length=50, null=True, blank=True)
    tarifa = models.CharField(max_length=70, null=True, blank=True)
    idbarrio = models.ForeignKey('Barrio', null=True, blank=True,
        db_column='idbarrio', verbose_name='barrio')
    iddepartamento = models.ForeignKey('Departamento', null=True, blank=True,
        db_column='iddepartamento', verbose_name='departamento')
    idmunicipio = models.ForeignKey('Municipio', null=True, blank=True,
        db_column='idmunicipio', verbose_name='municipio')
    servicio = models.CharField(max_length=70, null=True, blank=True)
    cupon = models.PositiveIntegerField(null=True, blank=True)
    total_mes_factura = models.FloatField(null=True, blank=True)
    valor_pagar = models.FloatField(null=True, blank=True)
    numero_fiscal = models.PositiveIntegerField(null=True, blank=True)
    factura_interna = models.PositiveIntegerField(null=True, blank=True)
    telefono_contacto = models.CharField(max_length=1000, null=True, blank=True)
    entrega = models.NullBooleanField(default=False,
        verbose_name='Comprobante POD')
    comprobante = models.FileField(upload_to=generar_ruta_comprobante,
        null=True, blank=True)
    cerrado = models.NullBooleanField(default=False)
    barra = models.CharField(max_length=30, null=True, blank=True)
    orden_impresion = models.PositiveIntegerField(null=True, blank=True)
    idcliente = models.IntegerField(null=True, blank=True,
        db_column='idcliente')
    entrega_numero = models.IntegerField(null=True, blank=True,
        verbose_name='numero de rendicion')
    tipificacion = models.ForeignKey('Tipificacion', null=True, blank=True)
    exportado = models.NullBooleanField(default=False,
        verbose_name='Aplicacion Movil')
    indexacion = models.IntegerField(null=True, blank=True)
    position = GeopositionField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    parentezco = models.CharField(max_length=75, null=True, blank=True)
    recibe = models.CharField(max_length=75, null=True, blank=True)
    imagen = models.FileField(upload_to=get_media_url, null=True, blank=True)
    ESTADOS_DE_ENTREGA = (('ENTREGADO', 'ENTREGADO'),
                          ('PENDIENTE', 'PENDIENTE'),
                          ('REZAGADO', 'REZAGADO'),
                         )
    estado = models.CharField(max_length=65, null=True, blank=True,
        choices=ESTADOS_DE_ENTREGA)
    fecha_asignacion_user = models.DateField(null=True, blank=True)

    def get_estado(self):
        if self.comprobante:
            return "ENTREGADO"
        else:
            if self.position and self.fecha_entrega and self.tipificacion:
                if self.tipificacion == Tipificacion.objects.get(id=1):
                    return "ENTREGADO"
                else:
                    return "REZAGADO"
            else:
                return "PENDIENTE"

    def get_telefono(self):
        telefonos = []
        if self.telefono:
            telefonos.append(self.telefono)
        if self.telefono_contacto:
            telefonos.append(self.telefono_contacto)
        if len(telefonos) > 0:
            return ', '.join(telefonos)
        else:
            return ''

    def link_comprobante(self):
        if self.comprobante:
            return '<a href="/media/%s" target="blank" onclick="return showAddAnotherPopup(this);">%s</a>' % (self.comprobante,
                'comprobante')
        else:
            return None

    link_comprobante.short_description = 'comprobante'
    link_comprobante.allow_tags = True

    def __unicode__(self):
        if self.factura:
            return self.factura
        else:
            return 'Paquete Oject'

    def integrar(self):
        if not self.iddepartamento:
            self.iddepartamento = self.get_departamento()
        if not self.idmunicipio:
            self.idmunicipio = self.get_municipio()
        if not self.idbarrio:
            self.idbarrio = self.get_barrio()
        if not self.idcliente:
            self.idcliente = self.get_cliente()
        self.barra = self.get_barra()

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

    def get_cliente(self):
        c = None
        if self.cliente and self.contrato and self.idbarrio \
        and self.idmunicipio and self.iddepartamento:
            try:
                c, created = Cliente.objects.get_or_create(name=self.cliente,
                    contrato=self.contrato, barrio=self.idbarrio,
                    municipio=self.idmunicipio,
                    departamento=self.iddepartamento)
            except:
                c = Cliente.objects.filter(name=self.cliente,
                    contrato=self.contrato, barrio=self.idbarrio,
                    municipio=self.idmunicipio,
                    departamento=self.iddepartamento)[0]
            c.direccion = self.direccion
            c.distribuidor = self.distribuidor
            c.telefono_contacto = self.get_telefono()
            c.tarifa = self.tarifa
            c.segmento = self.segmento
            c.servicio = self.servicio
            c.valor_pagar = self.valor_pagar
            c.save(0)
        return c

    def get_lotificado(self):
        if self.lote:
            return True
        else:
            return False

    def get_entregado(self):
        if self.comprobante:
            return True
        else:
            return False

    def get_barra(self):
        if self.contrato and self.ciclo and self.mes and self.ano:
            return str(self.contrato) + str(self.ciclo).zfill(2) \
            + str(self.mes).zfill(2) \
            + str(self.ano)
        else:
            return ''

    def get_colector(self):
        if self.entrega:
            pass
        else:
            if self.lote and self.lote.asignado():
                return self.lote.colector
            else:
                return None

    def name_file(self):
        return str(self.contrato) + str(self.ciclo).zfill(2) \
             + str(self.mes).zfill(2) + str(self.ano)[2:4]

    def temp_path(self):
        return os.path.join('TEMP', self.name_file() + '.pdf')

    def full_path(self):
        return os.path.join(get_ruta(self), self.name_file() + '.pdf')

    def codificacion_ciclo(self):
        return str(self.ano)[2:] + str(self.mes).zfill(2) + \
            str(self.ciclo).zfill(2) + '_8_' + str(self.entrega_numero)

    def export_path(self):
        carpeta = os.path.join(settings.MEDIA_ROOT, 'TEMP',
            self.codificacion_ciclo())
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        return carpeta

    def export_path_pdf(self):
        carpeta = os.path.join(self.export_path(), 'Factura PDF')
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        return os.path.join(carpeta, self.name_file() + '.pdf')

    def export_path_index(self):
        carpeta = os.path.join(self.export_path(), 'Archivo de Carga',
            get_servicio(self.ciclo))
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        return os.path.join(carpeta, 'ci' + self.codificacion_ciclo() +
        '_rec_im.txt')

    def autoasignar(self):
        if self.idbarrio:
            zb = None
            try:
                zb = zona_barrio.objects.get(barrio=self.idbarrio)
            except:
                pass
            if zb:
                self.zona = zb.zona.id
                self.save()

    def save(self, *args, **kwargs):
        self.entrega = self.get_entregado()
        self.estado = self.get_estado()
        if not self.cerrado:
            self.cerrado = False
        super(Paquete, self).save()

    def hora_entrega(self):
        if self.fecha_entrega:
            return self.fecha_entrega.strftime("%X")
        else:
            return None

    class Meta:
        verbose_name = 'factura'
        ordering = ['-fecha_entrega']


class Tipificacion(models.Model):
    causa = models.CharField(max_length=35, verbose_name="causa unificada")
    descripcion = models.TextField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.causa

    class Meta:
        verbose_name_plural = "tipificaciones"


class Departamento(Entidad):
    name_alt = models.CharField(max_length=75, null=True, blank=True,
        verbose_name="nombre alternativo",
        help_text="se usa para evitar la duplicidad")
    codigo_telefonico = models.CharField(max_length=5, null=True, blank=True)

    def crear_zona_master(self):
        mns = Municipio.objects.filter(departamento=self)
        if mns:
            zs = Zona.objects.filter(departamento=self)
            zs.delete()
            z = Zona()
            z.name = self.name
            z.departamento = self
            z.municipio = mns[0]
            z.save()
            codes = Barrio.objects.filter(
                departamento=self).values_list('code', flat=True)
            reasignar_barrios(z, codes)


class Municipio(Entidad):
    name_alt = models.CharField(max_length=75, null=True, blank=True,
        verbose_name="nombre alternativo",
        help_text="se usa para evitar la duplicidad")
    departamento = models.ForeignKey(Departamento, null=True, blank=True)


class Barrio(Entidad):
    departamento = models.ForeignKey(Departamento, null=True, blank=True)
    municipio = models.ForeignKey(Municipio, null=True, blank=True)
    relative_position = GeopositionField(null=True, blank=True)
    revizado = models.NullBooleanField()

    def __unicode__(self):
        return '%s-%s %s %s' % (smart_text(self.code), smart_text(self.name),
            smart_text(self.municipio.name),
            smart_text(self.departamento.name))

    def related_zones(self):
        return Zona.objects.filter(departamento=self.departamento)

    def to_json(self):
        obj = {}
        obj['id'] = self.id
        obj['code'] = self.code
        obj['name'] = self.name
        obj['departamento'] = self.departamento.name
        obj['municipio'] = self.municipio.name
        obj['referencias'] = []
        obj['zonas'] = []
        for d in Paquete.objects.filter(idbarrio=self):
            obj['referencias'].append(d.direccion)
        for z in self.related_zones():
            obj['zonas'].append([z.id, z.name])
        return obj

    def get_revizado(self):
        if self.relative_position:
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        self.revizado = self.get_revizado()
        super(Barrio, self).save()


class Zona(Entidad):
    departamento = models.ForeignKey(Departamento)
    municipio = models.ForeignKey(Municipio)

    def barrios(self):
        return Barrio.objects.filter(id__in=(zona_barrio.objects.filter(
            zona=self).values_list('barrio', flat=True)))

    def disponibles(self):
        return Barrio.objects.filter(departamento=self.departamento,
            municipio=self.municipio).exclude(id__in=(zona_barrio.objects.all(
            ).values_list('barrio', flat=True)))

    def autoasignar(self):
        if self.disponibles():
            for b in self.disponibles():
                zb, create = zona_barrio.objects.get_or_create(zona=self,
                    barrio=b)

    def add_barrio(self, barrio):
        zb, created = zona_barrio.objects.get_or_create(barrio=barrio)
        zb.zona = self
        zb.orden = None
        zb.save()


class zona_barrio(models.Model):
    zona = models.ForeignKey(Zona, null=True)
    barrio = models.ForeignKey(Barrio, null=True)
    orden = models.IntegerField(null=True)

    class Meta:
        unique_together = ('zona', 'barrio')
        verbose_name = 'barrio'
        verbose_name_plural = 'barrios incluidos'


class Cliente(Entidad):
    departamento = models.ForeignKey(Departamento, null=True, blank=True)
    municipio = models.ForeignKey(Municipio, null=True, blank=True)
    barrio = models.ForeignKey(Barrio, null=True, blank=True)
    contrato = models.PositiveIntegerField(null=True, blank=True)
    direccion = models.TextField(max_length=250, null=True, blank=True)
    distribuidor = models.CharField(max_length=150, null=True, blank=True)
    segmento = models.CharField(max_length=50, null=True, blank=True)
    tarifa = models.CharField(max_length=70, null=True, blank=True)
    servicio = models.CharField(max_length=70, null=True, blank=True)
    telefono_contacto = models.CharField(max_length=70, null=True, blank=True)
    valor_pagar = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwars):
        if not self.code:
            self.code = get_code_cliente(self)
        super(Cliente, self).save()


class base_vista(models.Model):

    def save(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

    class Meta:
        abstract = True


class Estadistica(base_vista):
    ano = models.IntegerField(blank=True, null=True)
    mes = models.IntegerField(blank=True, null=True)
    ciclo = models.IntegerField(blank=True, null=True)
    departamento = models.ForeignKey(Departamento, blank=True, null=True,
        db_column='iddepartamento')
    municipio = models.ForeignKey(Municipio, blank=True, null=True,
        db_column='idmunicipio')
    total = models.FloatField(blank=True, null=True)
    entregados = models.FloatField(blank=True, null=True)
    pendientes = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'metropolitana_estadistica'
        verbose_name = 'estadisticas generales'


class EstadisticaDepartamento(base_vista):
    ano = models.IntegerField(blank=True, null=True)
    mes = models.IntegerField(blank=True, null=True)
    ciclo = models.IntegerField(blank=True, null=True)
    departamento = models.ForeignKey(Departamento, blank=True, null=True,
        db_column='iddepartamento')
    total = models.FloatField(blank=True, null=True)
    entregados = models.FloatField(blank=True, null=True)
    pendientes = models.FloatField(blank=True, null=True)
    estadisticaciclo = models.ForeignKey('EstadisticaCiclo')

    class Meta:
        managed = False
        db_table = 'metropolitana_estadistica_departamento'
        verbose_name = 'estadisticas por departamento'


class CiclosActivos(models.Manager):
    def get_queryset(self):
        return super(CiclosActivos, self).get_queryset().exclude(
            code__in=CicloCierre.objects.all().values_list('code', flat=True))


class EstadisticaCiclo(base_vista):
    code = models.CharField(max_length=6, primary_key=True)
    ano = models.IntegerField(blank=True, null=True)
    mes = models.IntegerField(blank=True, null=True)
    ciclo = models.IntegerField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    entregados = models.FloatField(blank=True, null=True,
        verbose_name="escaneados")
    pendientes = models.FloatField(blank=True, null=True)

    objects = models.Manager()
    activos = CiclosActivos()

    def __unicode__(self):
        return self.code

    def paquetes(self):
        return Paquete.objects.filter(ciclo=self.ciclo, mes=self.mes,
            ano=self.ano)

    def paquetes_rendidos(self):
        return self.paquetes().filter(
            entrega=True).exclude(entrega_numero=None)

    def rendidos(self):
        return self.paquetes_rendidos().count()

    def entregas(self):
        return self.paquetes_rendidos().filter(entrega=True).order_by(
            'entrega_numero').distinct('entrega_numero')

    def paquetes_por_rendir(self):
        return self.paquetes().filter(entrega=True, entrega_numero=None)

    def por_rendir(self):
        return self.paquetes_por_rendir().count()
    por_rendir.short_description = 'listos para rendir'

    def numeros_rendicion(self):
        return self.entregas().values_list('entrega_numero', flat=True)

    def rendiciones(self):
        data = []
        if self.entregas():
            for e in self.entregas():
                data.append((e.entrega_numero, (
                    self.paquetes().filter(entrega=True,
                    entrega_numero=e.entrega_numero).count())))
        return data
    rendiciones.short_description = 'numeros de entrega'

    def get_next(self):
        n = 0
        if self.rendiciones():
            for r in self.rendiciones():
                if r[0] > n:
                    n = r[0]
        return n + 1

    def crear_nueva_rendicion(self):
        n = None
        ps = Paquete.objects.filter(id__in=self.paquetes().filter(entrega=True
            ).values_list('id', flat=True))
        if self.paquetes_por_rendir():
            n = self.get_next()
            ps = Paquete.objects.filter(id__in=self.paquetes_por_rendir(
                ).values_list('id', flat=True))
            ps.update(entrega_numero=n)
        return(n, ps)

    def generar_rendicion(self, numero):
        ps = self.paquetes().filter(entrega_numero=numero)
        p = ps[0]
        if os.path.exists(p.export_path()):
            cm1 = "rm -rf %s" % p.export_path()
            os.system(cm1)
        crear_rendicion(ps)
        return p.codificacion_ciclo()

    def carpeta(self):
        carpeta = str(self.ano)[2:] + str(self.mes).zfill(2) \
        + str(self.ciclo).zfill(2)
        carpeta = os.path.join(settings.MEDIA_ROOT, 'POD', carpeta,
            'Factura PDF')
        return carpeta

    def en_carpeta(self):
        if os.path.exists(self.carpeta()):
            carpeta = str(self.ano)[2:] + str(self.mes).zfill(2) \
            + str(self.ciclo).zfill(2)
            carpeta = os.path.join(settings.MEDIA_ROOT, 'POD', carpeta,
                'Factura PDF')
            archivo_out = os.path.join(self.carpeta(), 'archivo_out')
            outfd = open(archivo_out, 'w+')
            p = subprocess.Popen(['ls', carpeta], stdout=subprocess.PIPE)
            subprocess.call(['wc', '-l'], stdin=p.stdout, stdout=outfd)
            outfd.close()
            fd = open(archivo_out, 'r')
            output = fd.read()
            fd.close()
            return output
        else:
            return 0

    def cumplimiento(self):
        if self.paquetes():
            cantidad_paquetes = int(self.paquetes().count())
            entregados = self.paquetes().filter(entrega=True).count()
            avance = str(((entregados * 100) /
            cantidad_paquetes)).zfill(3) \
            + ' %'
            return avance
        else:
            return 'no data'

    def alertas(self):
        alertas = []
        repetidos = []
        contratos = Paquete.objects.raw("select min(id) id,contrato, count(*) veces from metropolitana_paquete where ciclo = 55 and mes = 11 group by contrato having count(*) > 1")
        for c in contratos:
            if self.paquetes().filter(contrato=c.contrato).count() > 1:
                repetidos.append(str(c.contrato))
        if repetidos:
            alerta = 'Los contratos ' + ', '.join(repetidos) + " estan repetidos"
            alertas.append(alerta)
        return alertas

    def estadisticas(self):
        data = {}
        for e in Paquete.ESTADOS_DE_ENTREGA:
            data[str(e[0])] = self.paquetes().filter(estado=e[0]).count()
        return data

    def estadisticas_departamentos(self):
        data = []
        ds = Departamento.objects.all().order_by('name')
        for d in ds:
            esta = {'name': d.name}
            for e in Paquete.ESTADOS_DE_ENTREGA:
                esta[str(e[0])] = self.paquetes().filter(iddepartamento=d,
                estado=e[0]).count()
            data.append(esta)
        return data

    def estado(self):
        cc = None
        try:
            cc = CicloCierre.objects.get(code=self.code)
            if cc:
                return "CERRADO"
            else:
                return "EN EJECUCION"
        except:
            return "EN EJECUCION"

    class Meta:
        managed = False
        db_table = 'metropolitana_estadistica_ciclo'
        verbose_name = 'estadistica'


class CicloCierre(models.Model):
    code = models.CharField(max_length=6, null=True, blank=True)
    fecha_cierre = models.DateField(null=True, blank=True)
    cerrado = models.BooleanField(default=False)


def estado(paquete):
    clase = ""
    valor = ""
    if paquete.entrega:
        clase = "alert alert-success"
        valor = "ESCANEADO"
    else:
        clase = "alert alert-danger"
        valor = "NO ESCANEADO"
    return (clase, valor)


def corregir_ubicacion(comprobantes):
    mr = settings.MEDIA_ROOT
    for c in comprobantes:
        if c.comprobante:
            o = c.comprobante.path
            n = generar_ruta_comprobante(c, c.comprobante.name)
            d = os.path.join(mr, get_ruta(c))
            if not os.path.exists(d):
                os.makedirs(d)
            try:
                os.rename(o, os.path.join(mr, n))
            except:
                pass
            c.comprobante.name = n
            c.save()


def importar_media(comprobantes):
    mr = settings.MEDIA_ROOT
    for c in comprobantes:
        o = os.path.join(mr, c.temp_path())
        if os.path.exists(o):
            n = generar_ruta_comprobante(c, 'archivo.pdf')
            print c.cliente
            d = os.path.join(mr, get_ruta(c))
            if not os.path.exists(d):
                os.makedirs(d)
            os.rename(o, os.path.join(mr, n))
            c.comprobante.name = n
            c.save()


def verificar_media(comprobantes):
    for c in comprobantes:
        c.comprobante.name = c.full_path()
        c.save()
        o = c.comprobante.path
        if not os.path.exists(o):
            c.comprobante = None
            c.entrega = False
        else:
            c.entrega = True
        c.save()


def cargar_temporal(comprobantes):
    for c in comprobantes:
        if not c.entrega:
            c.comprobante.name = c.temp_path()
            c.entrega = True
            c.save()


def exportar_media(comprobantes):
    mr = settings.MEDIA_ROOT
    for c in comprobantes:
        if c.comprobante:
            o = c.comprobante.path
            if os.path.exists(o):
                shutil.copy(os.path.join(mr, c.comprobante.path),
                    os.path.join(mr, c.export_path_pdf()))


def exportar_media_temp(comprobantes):
    mr = settings.MEDIA_ROOT
    for c in comprobantes:
        if c.comprobante:
            o = c.comprobante.path
            if os.path.exists(o):
                shutil.copy(os.path.join(mr, c.comprobante.path),
                    os.path.join(mr, c.temp_path()))
    os.system("cd %s && tar -czvf export.tar.gz *.pdf && rm *.pdf"
    % os.path.join(mr, "TEMP"))


def crear_index(comprobantes):
    mr = settings.MEDIA_ROOT
    for c in comprobantes:
        f = open(os.path.join(mr, c.export_path_index()), 'a')
        f.write("%s|%s|%s|D:\CargasDip\Claro_Nicaragua\Acuses\%s\%s.pdf\r\n" %
        (c.contrato, c.factura, c.cliente.encode('ascii', 'ignore'),
            get_servicio(c.ciclo), c.name_file()))
        f.close()


def crear_rendicion(comprobantes):
    exportar_media(comprobantes)
    crear_index(comprobantes)
    return comprobantes


def integrar(ps):
    message = ""
    ds = ps.order_by('departamento').distinct('departamento')
    for d in ds:
        qs = ps.filter(departamento=d.departamento)
        qs.update(iddepartamento=d.get_departamento().id)
    ms = ps.order_by('departamento', 'municipio').distinct(
        'departamento', 'municipio')
    for m in ms:
        qs = ps.filter(departamento=m.departamento,
            municipio=m.municipio)
        qs.update(idmunicipio=m.get_municipio().id)
    bs = ps.order_by('departamento', 'municipio', 'barrio').distinct(
        'departamento', 'municipio', 'barrio')
    for b in bs:
        qs = ps.filter(departamento=b.departamento,
            municipio=b.municipio, barrio=b.barrio)
        qs.update(idbarrio=b.get_barrio().id)
    for  p in ps:
        p.barra = p.get_barra()
        p.save()
    message += "integrado, total de facturas = %s end %s departamentos" \
    % (str(ps.count()), str(ds.count()))
    return message


def lista_distribucion(comprobantes):
    data = []
    ds = comprobantes.order_by('archivo').distinct('archivo')
    for d in ds:
        qs = comprobantes.filter(archivo=d.archivo)
        cantidad = qs.count()
        inicia = qs.aggregate(Min('consecutivo'))['consecutivo__min']
        termina = qs.aggregate(Max('consecutivo'))['consecutivo__max']
        item = {'archivo': d.archivo, 'cantidad': cantidad, 'inicia': inicia,
            'termina': termina}
        data.append(item)
    return data


def get_username(p):
    name = ''
    if p.user:
        name = p.user.username
    return name


def estadisticas_por_departamento(ciclo, mes, ano, departamento):
    data = []
    ps = Paquete.objects.filter(ciclo=ciclo, mes=mes, ano=ano,
        iddepartamento=departamento)
    users = ps.distinct('user').order_by('user')
    for u in users:
        d = {'user': get_username(u)}
        d['entregado'] = ps.filter(user=u.user, estado='ENTREGADO').count()
        d['rezagado'] = ps.filter(user=u.user, estado='REZAGADO').count()
        d['pendiente'] = ps.filter(user=u.user, estado='PENDIENTE').count()
        data.append(d)
    return data


class upmanager(models.Manager):
    def get_queryset(self):
        return uPaquete.objects.filter(factura__in=
        Paquete.objects.filter(ciclo=77, mes=2, ano=2016)[:100].values_list('factura',
            flat=True))


class uPaquete(models.Model):
    id = models.CharField(max_length=70, primary_key=True, db_column='factura')
    #position = GeopositionField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    ESTADOS_DE_ENTREGA = (('ENTREGADO', 'ENTREGADO'),
                          ('PENDIENTE', 'PENDIENTE'),
                          ('REZAGADO', 'REZAGADO'),
                         )
    estado = models.CharField(max_length=65, null=True, blank=True,
        choices=ESTADOS_DE_ENTREGA)

    class Meta:
        db_table = 'metropolitana_paquete'
        managed = False


class entrega_diaria(models.Model):
    dia = models.DateField()
    username = models.CharField(max_length=75)
    departamento = models.CharField(max_length=75)
    entregas = models.IntegerField()
    rezago = models.IntegerField()

    def fecha(self):
        return str(1000*time.mktime(self.dia.timetuple()))

    class Meta:
        managed = False
        db_table = "entrega_diaria"


def reasignar_barrios(zona, barrios):
    anteriores = zona_barrio.objects.filter(zona=zona)
    anteriores.delete()
    for b in barrios:
        zb = zona_barrio(zona=zona, barrio=Barrio.objects.get(code=b))
        zb.save()


def get_zona(barrio):
    try:
        return Zona.objects.get(
            id=zona_barrio.objects.filter(barrio=barrio)[0].zona.id)
    except:
        return None