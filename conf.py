
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

SERVE_DIRECTORY_PATH = '/webapps/servator/serve/'

try:
    from conf_local import *
except ImportError:
    pass