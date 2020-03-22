from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'aaq%279%kq14!w%(2(^8n17#yt1f*4$j2lf7ksyj^tw6$y@6+n'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ALLOWED_HOSTS = ['*']

try:
    from .local import *
except ImportError:
    pass