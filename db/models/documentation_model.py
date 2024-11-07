from db.connection import get_db


def get_all_documentation():
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute('SELECT * FROM documentation')
        return cursor.fetchall()


def add_documentation(url, description, item_id):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(
            'INSERT INTO documentation (url, description, item_id) VALUES (?, ?, ?)',
            (url, description, item_id)
        )
    db.commit()
