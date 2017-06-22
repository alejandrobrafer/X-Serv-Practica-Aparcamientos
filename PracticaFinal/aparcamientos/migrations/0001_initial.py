# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aparcamiento',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('idEntidad', models.IntegerField()),
                ('nombre', models.CharField(max_length=32)),
                ('contentUrl', models.URLField(max_length=300)),
                ('descripcion', models.TextField()),
                ('barrio', models.CharField(max_length=32)),
                ('distrito', models.CharField(max_length=32)),
                ('nombreVia', models.CharField(max_length=64)),
                ('claseVial', models.CharField(max_length=32)),
                ('tipoNum', models.CharField(blank=True, max_length=32)),
                ('num', models.CharField(blank=True, max_length=32)),
                ('accesibilidad', models.IntegerField(choices=[(0, '0'), (1, '1')])),
                ('coordenadaX', models.PositiveIntegerField()),
                ('coordenadaY', models.PositiveIntegerField()),
                ('latitud', models.FloatField(null=True, blank=True)),
                ('longitud', models.FloatField(null=True, blank=True)),
                ('telefono', models.TextField()),
                ('email', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Cambio',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('usuario', models.CharField(max_length=32)),
                ('titulo', models.CharField(default='', max_length=64)),
                ('letra', models.CharField(null=True, blank=True, max_length=64)),
                ('color', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('texto', models.TextField()),
                ('aparcamiento', models.ForeignKey(to='aparcamientos.Aparcamiento')),
            ],
        ),
        migrations.CreateModel(
            name='Elegido',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('usuario', models.CharField(max_length=32)),
                ('fecha', models.DateField(auto_now=True)),
                ('aparcamiento', models.ForeignKey(to='aparcamientos.Aparcamiento')),
            ],
        ),
        migrations.CreateModel(
            name='Megusta',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('usuario', models.CharField(max_length=32)),
                ('aparcamiento', models.ForeignKey(to='aparcamientos.Aparcamiento')),
            ],
        ),
    ]
