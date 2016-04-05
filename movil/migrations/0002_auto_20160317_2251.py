# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0026_auto_20160317_1727'),
        ('movil', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='departamentos',
            field=models.ManyToManyField(to='metropolitana.Departamento', null=True, verbose_name=b'departamentos que atiende'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_supervisor',
            field=models.BooleanField(default=False, verbose_name=b'es un supervisor?'),
            preserve_default=True,
        ),
    ]
