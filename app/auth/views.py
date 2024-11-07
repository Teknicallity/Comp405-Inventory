from app.auth import auth
from db.models.user_model import add_user
from flask import render_template


@auth.route('/login', methods=['GET', 'POST'])
def login():
    pass


@auth.route('/logout', methods=['POST'])
def logout():
    pass
