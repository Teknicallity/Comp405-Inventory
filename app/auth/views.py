import flask
import flask_login

from app.auth import auth
from app import login_manager, bcrypt
from app.auth.forms import LoginForm
from db.models.user_model import get_user_by_username


@login_manager.user_loader
def load_user(username):
    return get_user_by_username(username)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    next = flask.request.args.get("next")  # Capturing 'next' for redirects

    if form.validate_on_submit():
        user = get_user_by_username(form.username.data)
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            flask_login.login_user(user, remember=True)
            flask.flash('Logged in successfully.')
            return flask.redirect(next or flask.url_for('main.index'))

        flask.flash('Invalid username or password.')

    return flask.render_template('login.html', form=form)


@auth.route('/logout', methods=['POST'])
@flask_login.login_required
def logout():
    flask_login.logout_user()
    next = flask.request.args.get("next")
    flask.flash('Logged out successfully.')
    return flask.redirect(next or flask.url_for('main.index'))
