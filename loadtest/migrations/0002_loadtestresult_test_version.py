# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loadtest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='loadtestresult',
            name='test_version',
            field=models.CharField(default=b'', max_length=10, choices=[(b'2.3', b'2.3'), (b'2.7', b'2.7'), (b'2.7', b'2.7')]),
        ),
    ]
