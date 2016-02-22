from django.db import models
from django.contrib.auth.models import User
from metropolitana.models import get_media_url, Zona


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    foto = models.ImageField(upload_to=get_media_url)
    zonas = models.ManyToManyField(Zona)
    celular = models.CharField(max_length=14, null=True)

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = "usuarios de entrega"