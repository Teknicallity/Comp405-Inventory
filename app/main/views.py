from flask_login import login_required, current_user
from flask import jsonify, render_template, abort

from app.main import main
from db.models.user_model import User


@main.route('/')
def index():
    return render_template('home.html')
