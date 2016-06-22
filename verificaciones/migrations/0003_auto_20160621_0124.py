# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('verificaciones', '0002_verificacion_vendedor'),
    ]

    operations = [
        migrations.AddField(
            model_name='verificacion',
            name='hasta_50',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='verificacion',
            name='mas_50',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
