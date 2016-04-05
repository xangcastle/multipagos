# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cartera', '0004_auto_20160317_0524'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='has_pend',
            field=models.BooleanField(default=False, verbose_name=b'con gestiones pendientes'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cliente',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
