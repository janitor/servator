
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

SERVE_DIRECTORY_PATH = '/Users/raman/Development/servator/serve'

SERVATOR_DOMAIN = '.servator.ws'


try:
    from conf_local import *
except ImportError:
    pass