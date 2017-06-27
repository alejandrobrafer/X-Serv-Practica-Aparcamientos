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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
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
                ('latitud', models.FloatField(blank=True, null=True)),
                ('longitud', models.FloatField(blank=True, null=True)),
                ('telefono', models.TextField()),
                ('email', models.TextField()),
                ('visitas', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Cambio',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=32)),
                ('titulo', models.CharField(max_length=64, default='')),
                ('letra', models.CharField(blank=True, max_length=64, null=True)),
                ('color', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField()),
                ('aparcamiento', models.ForeignKey(to='aparcamientos.Aparcamiento')),
            ],
        ),
        migrations.CreateModel(
            name='Elegido',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=32)),
                ('fecha', models.DateField(auto_now=True)),
                ('aparcamiento', models.ForeignKey(to='aparcamientos.Aparcamiento')),
            ],
        ),
        migrations.CreateModel(
            name='Megusta',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=32)),
                ('aparcamiento', models.ForeignKey(to='aparcamientos.Aparcamiento')),
            ],
        ),
    ]
