# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0010_auto_20150601_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='paquete',
            name='idcliente',
            field=models.ForeignKey(blank=True, to='metropolitana.Cliente', null=True),
            preserve_default=True,
        ),
    ]
