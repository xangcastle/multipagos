# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metropolitana', '0008_auto_20160622_0127'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='paquete',
            index_together=set([('barra',)]),
        ),
    ]
