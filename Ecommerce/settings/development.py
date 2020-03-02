from Ecommerce.settings.base import *
import environ

env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env('./.env')

# DATABASE CONFIG
DATABASES = {}
DATABASE_URL = env('DB_URL')
DATABASES['default'] = dj_database_url.parse(DATABASE_URL, conn_max_age=None)

# CACHE STORAGE USING REDIS
CACHE_TTL = 60 * 10 # 60 minutes | 1 hour
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
    }
}
