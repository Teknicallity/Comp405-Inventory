from .base import BaseConfig


class DevConfig(BaseConfig):
    TESTING = True

    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'password'
    MYSQL_DATABASE = 'inventory_system'

    @classmethod
    def init_app(cls, app):
        BaseConfig.init_app(app)
