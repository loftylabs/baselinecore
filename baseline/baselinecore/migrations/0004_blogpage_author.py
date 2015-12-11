# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('baselinecore', '0003_homepage_snippet'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
