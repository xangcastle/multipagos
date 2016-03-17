from django.db import models
from metropolitana.models import generar_ruta_comprobante, get_media_url
from django.contrib.auth.models import User
from metropolitana.models import Paquete, importar_media
from django.db.models import Max
from datetime import datetime
from multifilefield.models import MultiFileField
from metropolitana.indexacion import id_generator, preparar_carpeta
import os
from django.conf import settings


class Pod(models.Model):
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
    barra = models.CharField(max_length=30, null=True, blank=True)
    entrega = models.NullBooleanField(default=False, verbose_name='entregada')
    entrega_numero = models.IntegerField(null=True, blank=True,
        verbose_name='numero de rendicion')
    comprobante = models.FileField(upload_to=generar_ruta_comprobante,
        null=True, blank=True)
    indexacion = models.ForeignKey('Indexacion', null=True, blank=True,
        db_column='indexacion', on_delete=models.SET_NULL)
    exportado = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = "metropolitana_paquete"
        verbose_name = 'comprobante'
        verbose_name_plural = 'carga de imagenes manual'

    ordering = ['consecutivo']

    def __unicode__(self):
        return self.factura

    def get_entregado(self):
        if self.comprobante:
            return True
        else:
            return False

    def get_barra(self):
        if self.contrato and self.ciclo and self.mes and self.ano:
            return str(self.contrato) + str(self.ciclo) \
            + str(self.mes).zfill(2) \
            + str(self.ano)
        else:
            return ''

    def name_file(self):
        return str(self.contrato) + str(self.ciclo).zfill(2) \
             + str(self.mes).zfill(2) + str(self.ano)[2:4]

    def save(self, *args, **kwargs):
        self.entrega = self.get_entregado()
        self.exportado = False
        super(Pod, self).save()


class import_manager(models.Manager):

    def get_queryset(self):
        return super(import_manager, self).get_queryset().filter(id__in=[1, ])


class import_paquete(models.Model):
    archivo = models.CharField(max_length=100, null=True, blank=True)
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
    idbarrio = models.IntegerField(null=True, blank=True)
    iddepartamento = models.IntegerField(null=True, blank=True)
    idmunicipio = models.IntegerField(null=True, blank=True)
    servicio = models.CharField(max_length=70, null=True, blank=True)
    cupon = models.PositiveIntegerField(null=True, blank=True)
    total_mes_factura = models.FloatField(null=True, blank=True)
    valor_pagar = models.FloatField(null=True, blank=True)
    numero_fiscal = models.PositiveIntegerField(null=True, blank=True)
    factura_interna = models.PositiveIntegerField(null=True, blank=True)
    telefono_contacto = models.CharField(max_length=70, null=True, blank=True)
    entrega = models.NullBooleanField(default=False, verbose_name='entregada')

    objects = models.Manager()
    objects = import_manager()

    class Meta:
        managed = False
        db_table = 'metropolitana_paquete'
        verbose_name = 'factura'
        verbose_name_plural = 'importacion de facturas'

    def save(self, *args, **kargs):
        self.entrega = False
        super(import_paquete, self).save()


class Impresion(models.Model):
    user = models.ForeignKey(User)
    fecha_verificacion = models.DateTimeField(auto_now=True,
    verbose_name="fecha de carga")
    paquete = models.ForeignKey(Paquete)
    consecutivo = models.PositiveIntegerField()
    archivo = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return str(self.paquete)

    def cliente(self):
        return self.paquete.cliente

    cliente.allow_tags = True

    def grupo(self):
        return Impresion.objects.filter(user=self.user)

    def get_consecutivo(self):
        if self.grupo():
            return self.grupo().aggregate(
                Max('consecutivo'))['consecutivo__max'] + 1
        else:
            return 1

    def save(self, *args, **kwars):
        if not self.consecutivo:
            self.consecutivo = self.get_consecutivo()
        super(Impresion, self).save()

    class Meta:
        verbose_name_plural = 'impresion de comprobantes'
        ordering = ['consecutivo']
        db_table = 'metropolitana_impresion'


def imprimir(comprobantes, user):
    for p in comprobantes.order_by('consecutivo'):
        i = Impresion(user=user, fecha_verificacion=datetime.now(),
            paquete=p, consecutivo=p.consecutivo, archivo=p.archivo)
        i.save()


def get_path(indexacion, filename):
    return os.path.join(indexacion.path(), filename)


class Indexacion(models.Model):
    fecha = models.DateField(auto_now_add=True, null=True)
    archivos = MultiFileField(upload_to=get_path, null=True, blank=True)
    carpeta = models.CharField(max_length=8, null=True)
    make_ocr = models.BooleanField(default=False, verbose_name="hacer ocr")

    def path(self):
        return os.path.join(settings.MEDIA_ROOT, 'Indexacion', self.carpeta)

    def url(self):
        if not self.carpeta:
            self.carpeta = id_generator()
        return os.path.join('/media', 'Indexacion', self.carpeta)

    def comprobantes(self):
        return Pod.objects.filter(indexacion=self)

    def total(self):
        return self.comprobantes().count()

    def resumen_por_ciclo(self):
        data = []
        cls = self.comprobantes().distinct('ciclo').order_by('ciclo')
        for c in cls:
            data.append((c.ciclo, self.comprobantes(
                ).filter(ciclo=c.ciclo).count()))
        return data

    def pendientes(self):
        archivos = []
        path = self.path()
        if os.path.exists(path):
            archivos = sorted(os.listdir(path))
        return archivos

    def carga_manual(self):
        data = self.pendientes()
        return '<a href="/digitalizacion/carga_manual/%s/" target="blank">%s comprobantes</a>' % (self.id ,len(data))
    carga_manual.allow_tags = True
    carga_manual.short_description = "Archivos Pendientes"

    class Meta:
        verbose_name_plural = "carga de imagenes masiva"
        verbose_name = "archivos pdf"

    def __unicode__(self):
        return str(self.fecha) + " - " + str(self.carpeta)

    def save(self, *args, **kwargs):
        if not self.carpeta:
            self.carpeta = id_generator()
        super(Indexacion, self).save()
        preparar_carpeta(self.path())


class Tar(models.Model):
    archivos = MultiFileField(null=True, blank=True)
    aplicar_ocr = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "carga de archivos"
        verbose_name = "archivos"

    def __unicode__(self):
        return str(self.archivo)

    def path(self):
        path = os.path.join(settings.MEDIA_ROOT, get_media_url(self,
        'archivo.pdf'))
        path = path.replace(os.path.basename(path), '')
        path = path.replace(os.path.basename(path), '')
        return path

    def descomprimir_importar(self):
        TEMP = os.path.join(settings.MEDIA_ROOT, 'TEMP')
        cmd = "cd %s && tar -xzvf export.tar.gz && rm -rf export.tar.gz" % (TEMP)
        os.system(cmd)
        ps = Paquete.objects.filter(entrega=False)
        importar_media(ps)

    def save(self, *args, **kwargs):
        super(Tar, self).save()
        if self.archivo:
            self.descomprimir_importar()


class Empleado(models.Model):
    idempleado = models.PositiveIntegerField(null=True, blank=True,
        verbose_name="codigo de empleado")
    nombre = models.CharField(max_length=120, null=True, blank=True)
    cedula = models.CharField(max_length=14, null=True, blank=True)
    gerencia = models.CharField(max_length=65, null=True, blank=True)
    localidad = models.CharField(max_length=65, null=True, blank=True)
    ecuenta = models.FileField(upload_to=get_media_url, null=True,
        blank=True, verbose_name="estado de cuenta")

    def __unicode__(self):
        return self.nombre

    def link_ecuenta(self):
        if self.ecuenta:
            return '<a href="/media/%s" target="blank" onclick="return showAddAnotherPopup(this);">%s</a>' % (self.ecuenta,
                'ver estado de cuenta')
        else:
            return ''

    link_ecuenta.short_description = ''
    link_ecuenta.allow_tags = True