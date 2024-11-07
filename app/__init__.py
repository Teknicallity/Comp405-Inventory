from flask import Flask
from flask_wtf.csrf import CSRFProtect
from config import config

csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    csrf.init_app(app)

    from db import connection as db_connection
    db_connection.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
