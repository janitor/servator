
SERVE_DIRECTORY_PATH = '/Users/raman/Development/servator/serve'

SERVATOR_DOMAIN = '.serve.janitorrb.com'


try:
    from conf_local import *
except ImportError:
    pass