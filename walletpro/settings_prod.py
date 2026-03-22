"""
Production settings - Railway/Render pe use karo
"""
from .settings import *
import dj_database_url
import os

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Parse database URL from environment (Railway/Render auto-sets this)
DATABASES = {
    'default': dj_database_url.parse(os.environ['DATABASE_URL'])
}

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
