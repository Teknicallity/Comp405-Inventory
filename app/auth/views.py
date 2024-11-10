import flask
import flask_login

from app.auth import auth
from app import login_manager, bcrypt, debug_only
from app.auth.forms import LoginForm
from db.models.user_model import get_user_by_username, User


@login_manager.user_loader
def load_user(username):
    return get_user_by_username(username)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    next = flask.request.args.get("next")

    if flask.request.method == 'POST':
        if form.validate():
            user = get_user_by_username(form.username.data)

            if user:
                if bcrypt.check_password_hash(user.password_hash, form.password.data):
                    flask_login.login_user(user, remember=True)
                    # flask.flash('Logged in successfully.')
                    return flask.redirect(next or flask.url_for('main.index'))

        flask.flash('Invalid username or password.')
        return flask.redirect(flask.url_for('auth.login', next=next))
    return flask.render_template('login.html', form=form)


@auth.route('/logout', methods=['POST'])
@flask_login.login_required
def logout():
    flask_login.logout_user()
    next = flask.request.args.get("next")
    # flask.flash('Logged out successfully.')
    return flask.redirect(next or flask.url_for('main.index'))


@auth.route('/current_user', methods=['GET'])
@debug_only
def current_user_info():
    user: User = flask_login.current_user
    return f'''
    <table style="border: 1px solid black; ">
        <thead>
            <tr>
                <th>Current User</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Username</td>
                <td>{user.username}</td>
            </tr>
            <tr>
                <td>Is Admin</td>
                <td>{user.is_admin}</td>
            </tr>
            <tr>
                <td>Employee Id</td>
                <td>{user.employee_id}</td>
            </tr>
        </tbody>
    </table>
    '''
