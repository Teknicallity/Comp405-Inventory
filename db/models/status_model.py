from db.connection import get_db


class StatusModel:
    def __init__(self, status_id, status_name):
        self.status_id = status_id
        self.status_name = status_name

    @classmethod
    def from_row(cls, row):
        return cls(
            status_id=row[0],
            status_name=row[1],
        ) if row else None

    @classmethod
    def list_from_rows(cls, rows):
        return [cls.from_row(row) for row in rows]

    def to_dict(self):
        return {
            'status_id': self.status_id,
            'status_name': self.status_name
        }


def get_all_statuses():
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute('SELECT status_id, name FROM statuses')
        return StatusModel.list_from_rows(cursor.fetchall())


def get_status_by_id(status_id: int):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute('SELECT status_id, name FROM statuses WHERE status_id = ?', (status_id,))
        return StatusModel.from_row(cursor.fetchone())


def add_status(status_name):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(
            'INSERT INTO statuses (name) VALUES (?)',
            (status_name,)
        )
    db.commit()
