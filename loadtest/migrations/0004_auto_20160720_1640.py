# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loadtest', '0003_auto_20160720_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loadtestresult',
            name='test_result_bitrate',
            field=models.TextField(default=b''),
        ),
        migrations.AlterField(
            model_name='loadtestresult',
            name='test_result_error',
            field=models.TextField(default=b'', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='loadtestresult',
            name='test_result_index',
            field=models.TextField(default=b''),
        ),
    ]
