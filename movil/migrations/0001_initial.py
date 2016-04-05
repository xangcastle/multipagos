# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import metropolitana.models


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0023_auto_20160317_0221'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('foto', models.ImageField(null=True, upload_to=metropolitana.models.get_media_url, blank=True)),
                ('celular', models.CharField(max_length=14, null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, help_text=b'el usuaro que anda el movil')),
                ('zonas', models.ManyToManyField(to='metropolitana.Zona', null=True, blank=True)),
            ],
            options={
                'verbose_name': 'usuario',
                'verbose_name_plural': 'usuarios de entrega',
            },
            bases=(models.Model,),
        ),
    ]
