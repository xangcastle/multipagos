# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cartera', '0006_auto_20160317_0717'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gestion',
            options={'verbose_name_plural': 'gestiones'},
        ),
        migrations.AlterModelOptions(
            name='tipogestion',
            options={'verbose_name': 'tipo de gestion', 'verbose_name_plural': 'tipos de gestiones'},
        ),
        migrations.AlterField(
            model_name='gestion',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
