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
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('idEntidad', models.IntegerField()),
                ('nombre', models.CharField(max_length=32)),
                ('contentUrl', models.URLField(max_length=32)),
                ('nombreVia', models.CharField(max_length=64)),
                ('claseVial', models.CharField(max_length=32)),
                ('tipoNum', models.CharField(blank=True, max_length=32)),
                ('num', models.CharField(blank=True, max_length=32)),
                ('descripcion', models.TextField()),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
                ('barrio', models.CharField(max_length=32)),
                ('distrito', models.CharField(max_length=32)),
                ('accesibilidad', models.IntegerField(choices=[(0, '0'), (1, '1')])),
                ('telefono', models.CharField(default='S/T', max_length=40)),
                ('email', models.EmailField(blank=True, max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Cambio',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('titulo', models.CharField(default='', max_length=64)),
                ('letra', models.IntegerField()),
                ('color', models.CharField(max_length=32)),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('texto', models.TextField()),
                ('usuario', models.CharField(max_length=32)),
                ('fecha', models.DateField(auto_now=True)),
                ('aparcamiento', models.ForeignKey(to='aparcamientos.Aparcamiento')),
            ],
        ),
        migrations.CreateModel(
            name='Elegido',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('usuario', models.CharField(max_length=32)),
                ('fecha', models.DateField(auto_now=True)),
                ('aparcamiento', models.ForeignKey(to='aparcamientos.Aparcamiento')),
            ],
        ),
    ]
