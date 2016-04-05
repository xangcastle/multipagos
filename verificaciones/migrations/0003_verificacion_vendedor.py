# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('verificaciones', '0002_auto_20160317_0221'),
    ]

    operations = [
        migrations.AddField(
            model_name='verificacion',
            name='vendedor',
            field=models.CharField(max_length=165, null=True, blank=True),
            preserve_default=True,
        ),
    ]
