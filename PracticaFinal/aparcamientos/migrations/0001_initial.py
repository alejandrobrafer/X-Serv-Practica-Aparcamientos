# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('tipoNum', models.CharField(max_length=32, blank=True)),
                ('num', models.CharField(max_length=32, blank=True)),
                ('accesibilidad', models.IntegerField(choices=[(0, '0'), (1, '1')])),
                ('coordenadaX', models.PositiveIntegerField()),
                ('coordenadaY', models.PositiveIntegerField()),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
                ('telefono', models.TextField()),
                ('email', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Cambio',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('titulo', models.CharField(max_length=64, default='')),
                ('letra', models.IntegerField()),
                ('color', models.CharField(max_length=32)),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('texto', models.TextField()),
                ('usuario', models.CharField(max_length=32)),
                ('fecha', models.DateField(auto_now=True)),
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
    ]
