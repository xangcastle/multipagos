# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0007_reenvioclaro_estado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reenvioclaro',
            name='estado',
        ),
        migrations.AddField(
            model_name='reenvioclaro',
            name='paquete',
            field=models.ForeignKey(blank=True, to='metropolitana.Paquete', null=True),
            preserve_default=True,
        ),
    ]
