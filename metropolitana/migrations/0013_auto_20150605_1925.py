# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0012_estadistica'),
    ]

    operations = [
        migrations.CreateModel(
            name='import_paquete',
            fields=[
            ],
            options={
                'db_table': 'metropolitana_paquete',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='paquete',
            options={'ordering': ['cliente'], 'verbose_name': 'factura'},
        ),
        migrations.RemoveField(
            model_name='paquete',
            name='estado',
        ),
        migrations.RemoveField(
            model_name='paquete',
            name='pod',
        ),
        migrations.AlterField(
            model_name='paquete',
            name='cerrado',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='paquete',
            name='entrega',
            field=models.NullBooleanField(default=False, verbose_name=b'entregada'),
        ),
        migrations.AlterField(
            model_name='paquete',
            name='lotificado',
            field=models.NullBooleanField(default=False),
        ),
    ]
