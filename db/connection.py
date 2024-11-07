import os.path
import click
import pymysql
from flask import current_app, g
from pymysql import OperationalError


def get_db():
    """Establish and return a database connection, caching it in the global object."""
    if 'db' not in g:
        g.db = pymysql.connect(
            host=current_app.config['MYSQL_HOST'],
            port=current_app.config['MYSQL_PORT'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DATABASE'],
            # ssl_verify_identity=True,
            # ssl_ca='SSL/certs/ca-cert.pem'
        )
    return g.db


def _get_db_server():
    return pymysql.connect(
        host=current_app.config['MYSQL_HOST'],
        port=current_app.config['MYSQL_PORT'],
        user=current_app.config['MYSQL_USER'],
        password=current_app.config['MYSQL_PASSWORD'],
    )


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def _apply_db_schema():
    db = get_db()
    schema_path = os.path.join(
        current_app.config['BASEDIR'],
        current_app.config.get('SCHEMA_FILE', 'setup-inventory.sql')
    )

    try:
        _execute_sql_file(db, schema_path)
    except FileNotFoundError:
        click.echo(f"Schema file {schema_path} not found.")
    except OperationalError as e:
        click.echo(f"Error applying schema: {e}")
        raise e
    else:
        db.commit()


def _execute_sql_file(db, filepath):
    with current_app.open_resource(filepath) as f:
        sql_commands = f.read().decode('utf8').split(';')
        with db.cursor() as cursor:
            for command in sql_commands:
                if command.strip():
                    cursor.execute(command)


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


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def _execute_db_command(command):
    """Execute a SQL command on the server connection without a specific database."""
    with _get_db_server() as connection:
        with connection.cursor() as cursor:
            cursor.execute(command)
            connection.commit()


def _create_database():
    _execute_db_command(f'CREATE DATABASE IF NOT EXISTS `{current_app.config['MYSQL_DATABASE']}`')


def _destroy_database():
    _execute_db_command(f'DROP DATABASE IF EXISTS `{current_app.config['MYSQL_DATABASE']}`')
