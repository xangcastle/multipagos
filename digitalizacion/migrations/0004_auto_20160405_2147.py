# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digitalizacion', '0003_auto_20151215_0237'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tar',
            name='archivo',
        ),
        migrations.AlterField(
            model_name='indexacion',
            name='fecha',
            field=models.DateField(auto_now_add=True, null=True),
            preserve_default=True,
        ),
    ]
