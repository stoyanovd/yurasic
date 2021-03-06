# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-11 20:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songsapp', '0005_auto_20171111_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='tags',
            field=models.ManyToManyField(blank=True, to='songsapp.Tag'),
        ),
        migrations.AlterField(
            model_name='realization',
            name='tags',
            field=models.ManyToManyField(blank=True, to='songsapp.Tag'),
        ),
        migrations.AlterField(
            model_name='song',
            name='tags',
            field=models.ManyToManyField(blank=True, to='songsapp.Tag'),
        ),
    ]
