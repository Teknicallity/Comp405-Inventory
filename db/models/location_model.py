from db.connection import get_db


def get_all_locations():
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(f'SELECT * FROM locations')
        return cursor.fetchall()


def get_location_by_id(location_id: int):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(f'SELECT * FROM locations WHERE location_id={location_id}')
        return cursor.fetchone()[1]


def add_location(location_name):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(
            f'INSERT INTO locations (name) VALUES (?)',
            (location_name,)
        )
    db.commit()