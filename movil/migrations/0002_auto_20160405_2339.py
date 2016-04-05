# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0002_auto_20160405_2339'),
        ('cartera', '0002_auto_20160405_2339'),
        ('movil', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'usuario', 'verbose_name_plural': 'usuarios de app movil'},
        ),
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
        migrations.AddField(
            model_name='userprofile',
            name='tipo_gestion',
            field=models.ManyToManyField(to='cartera.TipoGestion', null=True, verbose_name=b'tipos de gestiones que realiza', blank=True),
            preserve_default=True,
        ),
    ]
