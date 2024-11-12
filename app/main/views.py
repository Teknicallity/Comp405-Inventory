from flask_login import login_required, current_user
from flask import jsonify, render_template, abort

from app import debug_only
from app.main import main
from db.models.user_model import User


@main.route('/')
def index():
    return render_template('home.html')


@main.route('/test')
@debug_only
def test():
    return render_template('test.html')
