# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cartera', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='import_model',
            options={'verbose_name': 'registro', 'verbose_name_plural': 'importacion de datos'},
        ),
        migrations.RenameField(
            model_name='factura',
            old_name='idcliente',
            new_name='cliente',
        ),
        migrations.RenameField(
            model_name='factura',
            old_name='idtipo_mora',
            new_name='tipo_mora',
        ),
    ]
