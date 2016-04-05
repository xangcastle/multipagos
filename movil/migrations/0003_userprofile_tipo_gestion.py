# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cartera', '0010_auto_20160331_1630'),
        ('movil', '0002_auto_20160317_2251'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='tipo_gestion',
            field=models.ManyToManyField(to='cartera.TipoGestion', null=True, verbose_name=b'tipos de gestiones que realiza', blank=True),
            preserve_default=True,
        ),
    ]
