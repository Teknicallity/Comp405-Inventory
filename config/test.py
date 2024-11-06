from .base import BaseConfig


class TestConfig(BaseConfig):
    @classmethod
    def init_app(cls, app):
        BaseConfig.init_app(app)
