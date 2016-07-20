# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loadtest', '0002_loadtestresult_test_version'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loadtestresult',
            old_name='test_result',
            new_name='test_result_bitrate',
        ),
        migrations.AddField(
            model_name='loadtestresult',
            name='test_result_error',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='loadtestresult',
            name='test_result_index',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='loadtestresult',
            name='test_version',
            field=models.CharField(default=b'2.7', max_length=10, choices=[(b'2.3', b'2.3'), (b'2.7', b'2.7'), (b'2.8', b'2.8')]),
        ),
    ]
