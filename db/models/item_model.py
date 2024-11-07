from db.connection import get_db


def get_all_items():
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute('SELECT * FROM items')
        return cursor.fetchall()


def add_item(name, brand, model_number, serial_number):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(
            'INSERT INTO items (name, brand, model_number, serial_number) VALUES (?, ?, ?, ?)',
            (name, brand, model_number, serial_number)
        )
    db.commit()
