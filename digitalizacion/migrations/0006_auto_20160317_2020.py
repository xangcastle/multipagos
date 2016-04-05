# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digitalizacion', '0005_auto_20160317_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indexacion',
            name='fecha',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
    ]
