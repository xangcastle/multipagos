# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cartera', '0002_auto_20160405_2339'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewGestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contrato_cliente', models.CharField(max_length=65, null=True, blank=True)),
                ('user_id', models.CharField(max_length=65, null=True, blank=True)),
                ('gestion_code', models.CharField(max_length=65, null=True, blank=True)),
                ('fecha_asignacion', models.DateField(null=True)),
                ('fecha_vence', models.DateField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
