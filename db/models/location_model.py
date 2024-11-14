from db.connection import get_db


class LocationModel:
    def __init__(self, location_id, location_name):
        self.location_id = location_id
        self.location_name = location_name

    @classmethod
    def from_row(cls, row):
        return cls(
            location_id=row[0],
            location_name=row[1],
        ) if row else None

    @classmethod
    def list_from_rows(cls, rows):
        return [cls.from_row(row) for row in rows]

    def to_dict(self):
        return {
            'location_id': self.location_id,
            'location_name': self.location_name
        }


def get_all_locations():
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(f'SELECT location_id, name FROM locations')
        return LocationModel.list_from_rows(cursor.fetchall())


def get_location_by_id(location_id: int):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute('SELECT location_id, name FROM locations WHERE location_id = ?', (location_id,))
        return LocationModel.from_row(cursor.fetchone())


def add_location(location_name):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(
            f'INSERT INTO locations (name) VALUES (?)',
            (location_name,)
        )
    db.commit()
