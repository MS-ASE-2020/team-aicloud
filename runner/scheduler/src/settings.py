import os

try:
    from common.settings import *
except ImportError:
    pass

CONNECTION_STR = 'mysql+pymysql://root:66666666@mysql/rishi'

REDIS_HOST = '10.150.145.214'

REDIS_PORT = '7000'
