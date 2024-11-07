from db.connection import get_db


def get_all_employees():
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute('SELECT * FROM items')
        return cursor.fetchall()


def add_employee(first_name, last_name, title, reports_to_id=None):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(
            'INSERT INTO employees (first_name, last_name, title, reports_to) VALUES (?, ?, ?, ?)',
            (first_name, last_name, title, reports_to_id)
        )
    db.commit()
