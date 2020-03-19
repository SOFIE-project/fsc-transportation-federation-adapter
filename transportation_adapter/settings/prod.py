from .base import *

ALLOWED_HOSTS = ['*']

DEBUG = False

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Project wide settings
PROXY_PREFIX = 'transportation'   # no end slashes, set to `None` when not used

EXTERNAL_BASE_URI = 'https://192.168.1.167'

if PROXY_PREFIX:
    STATIC_URL = '/' + PROXY_PREFIX + STATIC_URL
    EXTERNAL_BASE_URI += '/{}'.format(PROXY_PREFIX)

THING_DESCRIPTION_PATH = os.path.join(BASE_DIR, 'td.json')

ETHEREUM_WALLET_PATH = os.path.join(BASE_DIR, 'config/wallet/keyfile.json')
ETHEREUM_WALLET_PASSWORD_PATH = os.path.join(BASE_DIR, 'config/wallet/password.txt')

# Redis settings
REDIS_HOST = 'transportation-adapter-redis'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_DATABASE = 0

# Mongo settings
MONGODB_HOST = '192.168.1.167'
MONGODB_PORT = 27017
MONGODB_USER = None
MONGODB_PASSWORD = None
MONGODB_DATABASE = 'kaa'
MONGODB_COLLECTION = 'logs_92794150186879175423'

# Swagger settings
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    #'DEFAULT_API_URL': EXTERNAL_BASE_URI
}
