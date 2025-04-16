from .base import *

ALLOWED_HOSTS = ['api.nursinghome.ai', ]
STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = []

DEBUG = False

CORS_ALLOWED_ORIGINS = [
    'http://3.36.24.37',
    'https://3.36.24.37',
    'http://nursinghome.ai',
    'https://nursinghome.ai',
    'http://api.nursinghome.ai',
    'https://api.nursinghome.ai',
]