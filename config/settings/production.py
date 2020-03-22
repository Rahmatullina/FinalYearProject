from __future__ import absolute_import, unicode_literals

from .base import *

env = os.environ.copy()

import dj_database_url

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY', default='aaq%279%kq14!w%(2(^8n17#yt1f*4$j2lf7ksyj^tw6$y@6+n')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ALLOWED_HOSTS = ['*']

if "DATABASE_URL" in env:
    DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

try:
    from .local import *
except ImportError:
    pass