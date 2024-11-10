from flask_login import UserMixin

from db.connection import get_db
from app import bcrypt


class User(UserMixin):
    def __init__(self, username, password_hash, is_admin, employee_id=None):
        self.username = username
        self.password_hash = password_hash
        self.is_admin = is_admin
        self.employee_id = employee_id

    def get_id(self):
        return self.username

    @classmethod
    def from_db_row(cls, row):
        return cls(
            username=row[1],
            password_hash=row[2],
            is_admin=row[3] == 1,
            employee_id=row[4]
        )

    @classmethod
    def list_from_rows(cls, rows):
        return [cls.from_db_row(row) for row in rows]

    def to_dict(self):
        return {
            'username': self.username,
            'is_admin': self.is_admin,
            'employee_id': self.employee_id
        }


def get_all_users():
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute('SELECT * FROM users')


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


def get_user_by_username(username) -> User:
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        row = cursor.fetchone()
        return User.from_db_row(row) if row else None


def get_admin_status(username):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        return cursor.fetchone()[3] == 1
