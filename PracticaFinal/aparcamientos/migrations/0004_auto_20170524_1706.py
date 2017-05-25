# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0003_auto_20170524_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aparcamiento',
            name='telefono',
            field=models.TextField(),
        ),
    ]
