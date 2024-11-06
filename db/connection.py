import os.path
import click
import pymysql
from flask import current_app, g

def get_db():
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

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    create_database()
    db = get_db()
    with current_app.open_resource(os.path.join(current_app.config['BASEDIR'], 'setup-inventory.sql')) as f:
        sql_commands = f.read().decode('utf8').split(';')
        with db.cursor() as cursor:
            for command in sql_commands:
                if command.strip():  # Skip empty commands
                    cursor.execute(command)
        db.commit()


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def create_database():
    connection = pymysql.connect(
        host=current_app.config['MYSQL_HOST'],
        port=current_app.config['MYSQL_PORT'],
        user=current_app.config['MYSQL_USER'],
        password=current_app.config['MYSQL_PASSWORD'],
    )

    with connection.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {current_app.config['MYSQL_DATABASE']}")
        connection.commit()

    connection.close()
