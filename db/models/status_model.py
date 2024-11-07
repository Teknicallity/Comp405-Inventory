from db.connection import get_db


def get_all_statuses():
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute('SELECT * FROM statuses')
        return cursor.fetchall()
