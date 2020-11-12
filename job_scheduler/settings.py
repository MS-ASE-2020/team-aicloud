import os

PORT = 12345

K8S_NAMESPACE = 'default'

IMAGE_NAME = ''

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATA_DIR = os.path.join(BASE_DIR, 'worker/data')
