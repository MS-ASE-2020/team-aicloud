import os

try:
    from common.settings import *
except ImportError:
    pass

CONNECTION_STR = 'mysql+pymysql://root:66666666@10.150.145.214:3306/rishi'

REDIS_HOST = 'redis'
