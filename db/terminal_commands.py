import click
from pymysql import OperationalError

from db.connection import _destroy_database, _create_database, _apply_db_schema
from db.models.user_model import add_user


@click.command('init-db')
@click.option('--reset', '-r', is_flag=True, default=False,
              help='Reset the database to a clean state before initialization')
def init_db_command(reset):
    """Command-line command to initialize the database."""
    if reset:
        _destroy_database()
        click.echo('Database deleted.')

    _create_database()

    try:
        _apply_db_schema()
    except OperationalError:
        click.echo('Pass -r or --reset flag to reset database.')
    else:
        click.echo('Initialized the database.')


@click.command('create-admin')
@click.option('--username', '-u', prompt='Admin Username', help='Admin Username')
def create_admin_command(username):
    password = click.prompt('Password', hide_input=True, confirmation_prompt=True)

    add_user(username, password, is_admin=True)
