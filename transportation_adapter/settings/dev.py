from .base import *

# Project wide settings
PROXY_PREFIX = 'transportation'   # no end slashes, set to `None` when not used

EXTERNAL_BASE_URI = 'http://localhost:8000'

if PROXY_PREFIX:
    EXTERNAL_BASE_URI += '/{}'.format(PROXY_PREFIX)

THING_DESCRIPTION_PATH = os.path.join(BASE_DIR, 'td.json')

# Redis settings
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_DATABASE = 0

# Mongo settings
MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_USER = None
MONGODB_PASSWORD = None
MONGODB_DATABASE = 'kaa'
MONGODB_COLLECTION = 'logs_92794150186879175423'

ETHEREUM_WALLET_PATH = os.path.join(BASE_DIR, 'config/wallet/keyfile.json')
ETHEREUM_WALLET_PASSWORD_PATH = os.path.join(BASE_DIR, 'config/wallet/password.txt')

# Indy settings
INDY_WALLET_PATH = os.path.join(BASE_DIR, 'config/indy')
INDY_WALLET_PASSWORD = SECRET_KEY

# PDS component settings
PDS_URI = 'http://127.0.0.1:9001'
