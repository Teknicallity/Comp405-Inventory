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

