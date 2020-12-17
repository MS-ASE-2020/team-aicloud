import os

try:
    from common.settings import *
except ImportError:
    pass

CONNECTION_STR = 'mysql+mysqldb://root:66666666@cloudai-rishi:3306/rishi'

REDIS_HOST = 'redis'
