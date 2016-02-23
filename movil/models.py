from django.db import models
from django.contrib.auth.models import User
from metropolitana.models import get_media_url, Zona


class UserProfile(models.Model):
    '''
    esta clase es la utilizada para guardar los perfiles de usuario
    '''
    user = models.OneToOneField(User, help_text="el usuaro que anda el movil")
    foto = models.ImageField(upload_to=get_media_url,
        null=True, blank=True)
    zonas = models.ManyToManyField(Zona)
    celular = models.CharField(max_length=14, null=True)

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = "usuarios de entrega"