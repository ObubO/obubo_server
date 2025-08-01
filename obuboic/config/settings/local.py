from .base import *
import pymysql
pymysql.install_as_MySQLdb()

ALLOWED_HOSTS = ['*']

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASAS": "djagno_redis.client.DefaultClient",
        }
    }
}