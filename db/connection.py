import os.path
import time

import click
import pymysql
from flask import current_app, g
from pymysql import OperationalError

MAX_RETRIES = 5
RETRY_DELAY = 2


def _connect_to_db(with_db_name=True):
    """
    Helper function to create a database connection with or without the config database name.
    """
    retries = 0
    while retries < MAX_RETRIES:
        try:
            return pymysql.connect(
                host=current_app.config['MYSQL_HOST'],
                port=current_app.config['MYSQL_PORT'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['MYSQL_DATABASE'] if with_db_name else None,
            )
        except OperationalError as e:
            retries += 1
            if retries >= MAX_RETRIES:
                click.echo("Failed to connect to the database after multiple attempts.")
                raise e
            else:
                click.echo(f"Connection failed ({retries}/{MAX_RETRIES}), retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)


def get_db():
    """Establish and return a database connection, caching it in the global object."""
    if 'db' not in g:
        g.db = _connect_to_db(with_db_name=True)
    return g.db


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


def _execute_db_command(command):
    """Execute a SQL command on the server connection without a specific database."""
    with _connect_to_db(with_db_name=False) as connection:
        with connection.cursor() as cursor:
            cursor.execute(command)
            connection.commit()


def _create_database():
    _execute_db_command(f'CREATE DATABASE IF NOT EXISTS `{current_app.config['MYSQL_DATABASE']}`')


def _destroy_database():
    _execute_db_command(f'DROP DATABASE IF EXISTS `{current_app.config['MYSQL_DATABASE']}`')
