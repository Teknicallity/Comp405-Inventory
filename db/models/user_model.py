from db.connection import get_db
from app import bcrypt


def add_user(username, password, is_admin, employee_id=None):
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(
            'INSERT INTO users (username, password_hash, is_admin, employee_id) VALUES (%s, %s, %s, %s)',
            (username, password_hash, is_admin, employee_id)
        )
    db.commit()


def user_exists(username):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        return cursor.fetchone() is not None


def get_admin_status(username):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        return cursor.fetchone()[3] == 1
