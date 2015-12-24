# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import geoposition.fields
import metropolitana.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('metropolitana', '0020_auto_20151009_0155'),
    ]

    operations = [
        migrations.AddField(
            model_name='paquete',
            name='fecha_entrega',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='paquete',
            name='imagen',
            field=models.FileField(null=True, upload_to=metropolitana.models.get_media_url, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='paquete',
            name='parentezco',
            field=models.CharField(max_length=25, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='paquete',
            name='position',
            field=geoposition.fields.GeopositionField(max_length=42, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='paquete',
            name='recibe',
            field=models.CharField(max_length=25, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='paquete',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
