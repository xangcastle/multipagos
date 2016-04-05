# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cartera', '0005_auto_20160317_0652'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='corte',
            name='barrio',
        ),
        migrations.RemoveField(
            model_name='corte',
            name='cliente',
        ),
        migrations.RemoveField(
            model_name='corte',
            name='departamento',
        ),
        migrations.RemoveField(
            model_name='corte',
            name='municipio',
        ),
        migrations.RemoveField(
            model_name='corte',
            name='user',
        ),
        migrations.RemoveField(
            model_name='corte',
            name='user_solicita',
        ),
        migrations.DeleteModel(
            name='Corte',
        ),
        migrations.AddField(
            model_name='factura',
            name='monto_abonado',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gestion',
            name='monto',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
    ]
