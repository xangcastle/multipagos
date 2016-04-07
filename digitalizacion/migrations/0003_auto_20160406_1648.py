# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digitalizacion', '0002_auto_20160405_2339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indexacion',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True, null=True),
            preserve_default=True,
        ),
    ]
