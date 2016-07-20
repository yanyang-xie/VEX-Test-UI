# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LoadTestResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('test_date', models.DateTimeField()),
                ('test_result', models.TextField()),
                ('test_type', models.CharField(default=b'VOD', max_length=100, choices=[(b'VOD', b'vod'), (b'cDVR', b'cdvr'), (b'Linear', b'linear')])),
            ],
            options={
                'db_table': 'load_test_result',
            },
        ),
    ]
