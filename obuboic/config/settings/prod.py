from .base import *

ALLOWED_HOSTS = ['3.38.12.213', 'nursinghome.ai', ]
STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = []

DEBUG = False

CORS_ALLOWED_ORIGINS = [
    'http://3.38.12.213',
    'https://3.38.12.213',
    'http://nursinghome.ai',
    'https://nursinghome.ai',
]