import settings
import os


class URLConstructor:
    @staticmethod
    def get_data_url(path):
        return os.path.join(settings.STATIC_PREFIX, path)