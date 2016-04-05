# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movil', '0003_userprofile_tipo_gestion'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'usuario', 'verbose_name_plural': 'usuarios de app movil'},
        ),
    ]
