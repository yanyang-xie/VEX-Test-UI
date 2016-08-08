# -*- coding=utf-8 -*-

"""
WSGI config for VEXTestUI project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# 将系统的编码设置为UTF8
reload(sys)
sys.setdefaultencoding('utf8')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VEXTestUI.settings")

application = get_wsgi_application()
