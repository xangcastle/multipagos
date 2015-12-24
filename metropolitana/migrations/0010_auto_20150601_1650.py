# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0009_auto_20150601_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paquete',
            name='idbarrio',
            field=models.ForeignKey(db_column=b'idbarrio', blank=True, to='metropolitana.Barrio', null=True),
        ),
        migrations.AlterField(
            model_name='paquete',
            name='iddepartamento',
            field=models.ForeignKey(db_column=b'iddepartamento', blank=True, to='metropolitana.Departamento', null=True),
        ),
        migrations.AlterField(
            model_name='paquete',
            name='idmunicipio',
            field=models.ForeignKey(db_column=b'idmunicipio', blank=True, to='metropolitana.Municipio', null=True),
        ),
    ]
