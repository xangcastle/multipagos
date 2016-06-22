# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0006_auto_20160621_0513'),
    ]

    operations = [
        migrations.AddField(
            model_name='reenvioclaro',
            name='estado',
            field=models.CharField(default=b'NINGUNO', max_length=50, blank=True),
            preserve_default=True,
        ),
    ]
