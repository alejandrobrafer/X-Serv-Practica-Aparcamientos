# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0002_auto_20170607_0355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cambio',
            name='letra',
            field=models.CharField(max_length=64, blank=True, null=True),
        ),
    ]
