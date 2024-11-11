import sys

import click
from pymysql import OperationalError
from flask import current_app

from db.connection import _destroy_database, _create_database, _apply_db_schema
from db.models.employee_model import add_employee, EmployeeModel
from db.models.user_model import add_user, user_exists


@click.command('init-db')
@click.option('--reset', '-r', is_flag=True, default=False,
              help='Reset the database to a clean state before initialization')
def init_db_command(reset):
    """Command-line command to initialize the database."""
    try:
        if reset:
            _destroy_database()
            click.echo('Database deleted.')

        _create_database()
        click.echo('Database created.')
    except OperationalError as e:
        click.echo(f'Could not connect to database: {e}', err=True)
        sys.exit(1)

    try:
        _apply_db_schema()
    except OperationalError:
        click.echo(f'Error applying schema: {e}', err=True)
        click.echo('Pass -r or --reset flag to reset database.')
    else:
        click.echo('Initialized the database.')


@click.command('create-admin')
@click.option('--username', '-u', prompt='Admin Username', help='Admin Username')
def create_admin_command(username):
    """Creates a user with admin privileges."""
    password = click.prompt('Password', hide_input=True, confirmation_prompt=True)
    add_user(
        username,
        password,
        is_admin=True,
    )


@click.command('ensure-admin')
def ensure_admin():
    """Creates an admin user from config or environment variables if user doesn't exist'."""
    if current_app.config['ADMIN_USER']:
        if not user_exists(current_app.config['ADMIN_USER']):

            add_user(
                current_app.config['ADMIN_USER'],
                current_app.config['ADMIN_PASSWORD'],
                True,
            )
            click.echo(f'Created admin user "{current_app.config['ADMIN_USER']}" from environment')
        else:
            click.echo('Environment defined admin user exists')
    else:
        click.echo('Environment admin user not defined')
