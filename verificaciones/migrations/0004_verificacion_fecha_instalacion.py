# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('verificaciones', '0003_auto_20160621_0124'),
    ]

    operations = [
        migrations.AddField(
            model_name='verificacion',
            name='fecha_instalacion',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
