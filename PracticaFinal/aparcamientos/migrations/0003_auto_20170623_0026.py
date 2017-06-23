# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0002_aparcamiento_megustas'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aparcamiento',
            old_name='megustas',
            new_name='visitas',
        ),
    ]
