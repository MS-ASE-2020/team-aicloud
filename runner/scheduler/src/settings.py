import os

try:
    from common.settings import *
except ImportError:
    pass

CONNECTION_STR = 'mysql+mysqldb://root:66666666@mysql/rishi'

REIDS_HOST = 'cloudai-rishi:6379'
