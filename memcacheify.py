from os import environ


# Memcache addon environment variables.
# See: https://addons.heroku.com/memcache
MEMCACHE_ENV_VARS = (
    'MEMCACHE_PASSWORD',
    'MEMCACHE_SERVERS',
    'MEMCACHE_USERNAME',
)


# MemCachier addon environment variables.
# See: https://addons.heroku.com/memcachier
MEMCACHIER_ENV_VARS = (
    'MEMCACHIER_PASSWORD',
    'MEMCACHIER_SERVERS',
    'MEMCACHIER_USERNAME',
)


def memcacheify():
    """Return a fully configured Django ``CACHES`` setting. We do this by
    analyzing all environment variables on Heorku, scanning for an available
    memcache addon, and then building the settings dict properly.

    If no memcache servers can be found, we'll revert to building a local
    memory cache.

    Returns a fully configured caches dict.
    """
    caches = {}

    if all((environ.get(e, '') for e in MEMCACHE_ENV_VARS)):
        caches['default'] = {
            'BACKEND': 'johnny.backends.memcached.MemcachedCache',
            'BINARY': True,
            'JOHNNY_CACHE': True,
            'LOCATION': 'localhost:11211',
            'OPTIONS': {
                'ketama': True,
                'tcp_nodelay': True,
            },
            'TIMEOUT': 500,
        }
    elif all((environ.get(e, '') for e in MEMCACHIER_ENV_VARS)):
        environ['MEMCACHE_SERVERS'] = environ.get('MEMCACHIER_SERVERS')
        environ['MEMCACHE_USERNAME'] = environ.get('MEMCACHIER_USERNAME')
        environ['MEMCACHE_PASSWORD'] = environ.get('MEMCACHIER_PASSWORD')
        caches['default'] = {
            'BACKEND': 'johnny.backends.memcached.MemcachedCache',
            'BINARY': True,
            'JOHNNY_CACHE': True,
            'LOCATION': environ.get('MEMCACHIER_SERVERS'),
            'OPTIONS': {
                'ketama': True,
                'tcp_nodelay': True,
            },
            'TIMEOUT': 500,
        }
    else:
        caches['default'] = {
            'BACKEND': 'johnny.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
            'JOHNNY_CACHE': True,
        }
    

    return caches
