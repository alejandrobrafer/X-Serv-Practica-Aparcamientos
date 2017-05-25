# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0002_auto_20170524_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aparcamiento',
            name='email',
            field=models.TextField(),
        ),
    ]
