from django.db import models
from django.contrib.auth.models import User
from metropolitana.models import get_media_url, Zona, Departamento
from cartera.models import TipoGestion


class UserProfile(models.Model):
    '''
    esta clase es la utilizada para guardar los perfiles de usuario
    '''
    user = models.OneToOneField(User, help_text="el usuaro que anda el movil")
    foto = models.ImageField(upload_to=get_media_url,
        null=True, blank=True)
    zonas = models.ManyToManyField(Zona, null=True, blank=True)
    tipo_gestion = models.ManyToManyField(TipoGestion, null=True, blank=True,
        verbose_name="tipos de gestiones que realiza")
    celular = models.CharField(max_length=14, null=True)
    is_supervisor = models.BooleanField(default=False,
        verbose_name="es un supervisor?")
    departamentos = models.ManyToManyField(Departamento, null=True,
        verbose_name="departamentos que atiende")

    def __unicode__(self):
        return "user " + self.user.username

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = "usuarios de app movil"

from math import radians, cos, sin, asin, sqrt


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371
    # Radius of earth in kilometers. Use 3956 for miles
    return c * r
