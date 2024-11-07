from db.connection import get_db


def get_all_checkouts():
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute('SELECT * FROM items')
        return cursor.fetchall()


def add_checkout(item_id, status_id, employee_id):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(
            'INSERT INTO checkouts (item_id, status_id, employee_id) VALUES (?, ?, ?)',
            (item_id, status_id, employee_id)
        )
    db.commit()


def return_checkout(item_id, status_id, employee_id):
    pass
