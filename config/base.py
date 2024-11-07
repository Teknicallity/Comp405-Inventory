import os


class BaseConfig:
    BASEDIR = os.path.dirname(os.path.dirname(__file__))
    FLASK_DEBUG = False
    TESTING = False
    SECRET_KEY = '319c7065fb0ee900ed6479466601f9ce1c21b1ef7fc6235105525ff77aaf1e62'

    @staticmethod
    def init_app(app):
        pass
