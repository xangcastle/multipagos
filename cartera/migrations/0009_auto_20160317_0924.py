# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cartera', '0008_auto_20160317_0821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='barrio',
            field=models.ForeignKey(related_name='cartera_cliente_barrio', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='metropolitana.Barrio', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cliente',
            name='departamento',
            field=models.ForeignKey(related_name='cartera_cliente_departamento', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='metropolitana.Departamento', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cliente',
            name='municipio',
            field=models.ForeignKey(related_name='cartera_cliente_municipio', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='metropolitana.Municipio', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cliente',
            name='tipo_mora',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='cartera.TipoMora', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cliente',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cliente',
            name='zona',
            field=models.ForeignKey(related_name='cartera_cliente_zona', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='metropolitana.Zona', null=True),
            preserve_default=True,
        ),
    ]
