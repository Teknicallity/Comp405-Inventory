from datetime import datetime

from db.connection import get_db


class CheckoutModel:
    def __init__(self, item_id, employee_id=None, checkout_date=None, returned_date: datetime = None, checkout_id=None):
        self.checkout_id = checkout_id
        self.item_id = item_id
        self.employee_id = employee_id
        self.checkout_date = checkout_date
        self.returned_date = returned_date

    @classmethod
    def from_row(cls, row):
        return cls(
            checkout_id=row[0],
            item_id=row[1],
            employee_id=row[2],
            checkout_date=row[3],
            returned_date=row[4]
        )

    @classmethod
    def list_from_rows(cls, rows) -> list:
        return [cls.from_row(row) for row in rows]

    def to_dict(self):
        return {
            'checkout_id': self.checkout_id,
            'item_id': self.item_id,
            'employee_id': self.employee_id,
            'checkout_date': self.checkout_date,
            'returned_date': self.returned_date,
        }


def get_all_checkouts() -> list:
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute('''
            SELECT c.checkout_id, c.item_id, c.employee_id, c.checkout_date, c.returned_date
            FROM checkouts c
        ''')
        return CheckoutModel.list_from_rows(cursor.fetchall())


def create_checkout(checkout: CheckoutModel) -> CheckoutModel:
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(
            'INSERT INTO checkouts (item_id, employee_id) VALUES (%s, %s)',
            (checkout.item_id, checkout.employee_id)
        )
        checkout_id = cursor.lastrowid
    db.commit()
    return get_checkout_by_id(checkout_id)  # status default


def get_checkout_by_id(checkout_id: int) -> CheckoutModel:
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute('''
            SELECT c.checkout_id, c.item_id, c.employee_id, c.checkout_date, c.returned_date
            FROM checkouts c
            WHERE checkout_id = %s
        ''', (checkout_id,))
        return CheckoutModel.from_row(cursor.fetchone())


def update_checkout(checkout: CheckoutModel):
    db = get_db()
    with db.cursor() as cursor:
        query = 'UPDATE checkouts SET'
        updates = []
        params = []

        if checkout.item_id is not None:
            updates.append(' item_id = %s')
            params.append(checkout.item_id)

        if checkout.employee_id is not None:
            updates.append(' employee_id = %s')
            params.append(checkout.employee_id)

        if updates:
            query += ','.join(updates) + ' WHERE checkout_id = %s'
            params.append(checkout.checkout_id)
            cursor.execute(query, tuple(params))
            db.commit()


def return_checkout(checkout_id: int) -> CheckoutModel:
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute('''UPDATE checkouts SET returned_date = NOW() WHERE checkout_id = %s''', (checkout_id,))
        db.commit()
    return get_checkout_by_id(checkout_id)


def delete_checkout(checkout_id: int):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute('DELETE FROM checkouts WHERE checkout_id = %s', (checkout_id,))
    db.commit()
