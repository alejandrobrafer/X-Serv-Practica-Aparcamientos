# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aparcamiento',
            name='claseVial',
        ),
        migrations.RemoveField(
            model_name='aparcamiento',
            name='idEntidad',
        ),
        migrations.RemoveField(
            model_name='aparcamiento',
            name='nombreVia',
        ),
        migrations.RemoveField(
            model_name='aparcamiento',
            name='num',
        ),
        migrations.RemoveField(
            model_name='aparcamiento',
            name='tipoNum',
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='contentUrl',
            field=models.URLField(max_length=300),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='telefono',
            field=models.IntegerField(),
        ),
    ]
