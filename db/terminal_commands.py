import csv
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
    except OperationalError as e:
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
            click.echo(f'Created admin user "{current_app.config["ADMIN_USER"]}" from environment')
        else:
            click.echo('Environment defined admin user exists')
    else:
        click.echo('Environment admin user not defined')


@click.command('create-employee')
@click.option('--file', '-F', type=click.Path(exists=True, dir_okay=False),
              help='CSV file with employees')
@click.option('--first', '-f', help='First Name (required if not using --file)')
@click.option('--last', '-l', help='Last Name (required if not using --file)')
@click.option('--title', '-t', help='Employee Title (required if not using --file)')
@click.option('--username', '-u', help='Username (required if not using --file)')
@click.option('--admin', '-a', is_flag=True, default=False, help='User is admin?')
def create_employee_command(file, first, last, title, username, admin):
    """
    Creates an employee or bulk creates employees from a CSV file.
    """
    if file:
        # Bulk creation from CSV
        try:
            with open(file, newline='') as csvfile:
                reader: csv.DictReader = csv.DictReader(csvfile)
                for row in reader:
                    _create_employee(
                        first_name=row.get('first_name'),
                        last_name=row.get('last_name'),
                        title=row.get('title'),
                        reports_to_id=int(row.get('reports_to_id', 0)) or None,
                        username=row.get('username'),
                        password=row.get('password'),
                        is_admin=row.get('is_admin', 'false').lower() == 'true'
                    )
            click.echo(f"Employees from {file} created successfully.")
        except Exception as e:
            click.echo(f"Error reading file: {e}")
    else:
        # Single employee creation
        if not (first and last and title and username):
            click.echo("Error: Missing required fields: --first, --last, --title, and --username.")
            return
        password = click.prompt('Password', hide_input=True, confirmation_prompt=True)
        _create_employee(first_name=first, last_name=last, title=title, username=username,
                         password=password, is_admin=admin)
        click.echo(f"Employee {first} {last} created successfully.")


def _create_employee(first_name, last_name, title, reports_to_id, username, password, is_admin):
    employee = EmployeeModel(
        first_name=first_name,
        last_name=last_name,
        title=title,
        reports_to=reports_to_id,
        username=username,
        password=password,
        is_admin=is_admin
    )
    add_employee(employee)
