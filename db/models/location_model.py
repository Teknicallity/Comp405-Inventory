from db.connection import get_db


def get_all_locations():
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(f'SELECT * FROM locations')
        return cursor.fetchall()


def add_location(location_name):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(
            f'INSERT INTO locations (name) VALUES (?)',
            (location_name,)
        )
    db.commit()