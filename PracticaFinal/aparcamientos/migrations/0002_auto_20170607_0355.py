# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aparcamiento',
            name='latitud',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='longitud',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='cambio',
            name='letra',
            field=models.IntegerField(max_length=64, null=True, blank=True),
        ),
    ]
