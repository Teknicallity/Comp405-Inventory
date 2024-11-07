from db.connection import get_db


def get_all_codes():
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute('SELECT * FROM qrcodes')
        return cursor.fetchall()


def add_code(uuid, item_id, created_date, last_used_date, created_by):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(
            'INSERT INTO qrcodes (uuid, item_id, created_date, last_used_date, created_by) VALUES (?, ?, ?, ?, ?)',
            (uuid, item_id, created_date, last_used_date, created_by)
        )
    db.commit()
