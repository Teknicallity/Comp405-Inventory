import os
import secrets

from .base import BaseConfig


class ProdConfig(BaseConfig):
    TESTING = False

    secret_key_path = os.path.join(BaseConfig.BASEDIR, 'data', 'secretkey.txt')
    try:
        with open(secret_key_path) as f:
            SECRET_KEY = f.read().strip()
    except FileNotFoundError:
        SECRET_KEY = secrets.token_hex()
        try:
            with open(secret_key_path, 'w', encoding='utf-8') as f:
                f.write(SECRET_KEY)
        except (OSError, IOError) as e:
            print(f"Error writing to {secret_key_path}: {e}")

    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    # DATABASE_CONNECTION = f"mysql://{MYSQL_HOST}:{MYSQL_PORT}"
    MYSQL_USER = os.environ.get('MYSQL_USER', 'your_user')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'your_password')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'your_db')

    ADMIN_USER = os.environ.get('ADMIN_USER', None)
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', None)
    RETRY_DB_CONNECTION = os.getenv("RETRY_DB_CONNECTION", True)

    @classmethod
    def init_app(cls, app):
        BaseConfig.init_app(app)
