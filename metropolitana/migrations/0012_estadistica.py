# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0011_paquete_idcliente'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estadistica',
            fields=[
            ],
            options={
                'db_table': 'metropolitana_estadistica',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
