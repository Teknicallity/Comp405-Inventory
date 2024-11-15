from flask import abort

from db.connection import get_db


class ItemModel:
    def __init__(self, name=None, brand=None, model=None, serial=None, item_id=None, location_id=None,
                 location_name=None, status_id=1, status_name=None):
        self.item_id = item_id
        self.name = name
        self.brand = brand
        self.model = model
        self.serial = serial
        self.location_id = location_id
        self.location_name = location_name
        self.status_id = status_id
        self.status_name = status_name

    @classmethod
    def from_row(cls, row):
        return cls(
            item_id=row[0],
            name=row[1],
            brand=row[2],
            model=row[3],
            serial=row[4],
            location_id=row[5],
            location_name=row[6],
            status_id=row[7],
            status_name=row[8]
        ) if row else None

    @classmethod
    def list_from_rows(cls, rows) -> list:
        return [cls.from_row(row) for row in rows]

    def to_dict(self):
        # Convert the object attributes to a dictionary
        return {
            "item_id": self.item_id,
            "name": self.name,
            "brand": self.brand,
            "model": self.model,
            "serial": self.serial,
            "location_id": self.location_id,
            "location_name": self.location_name,
            "status_id": self.status_id,
            "status_name": self.status_name
        }


def get_all_items():
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute('''
            SELECT i.item_id, i.name, i.brand, i.model, i.serial, i.location_id, l.name, i.status_id, s.name
            FROM items i
            LEFT JOIN locations l ON i.location_id = l.location_id
            LEFT JOIN statuses s ON i.status_id = s.status_id
        ''')
        return ItemModel.list_from_rows(cursor.fetchall())


def get_item_by_id(item_id: int):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(f'''
            SELECT i.item_id, i.name, i.brand, i.model, i.serial, i.location_id, l.name, i.status_id, s.name
            FROM items i
            LEFT JOIN locations l ON i.location_id = l.location_id
            LEFT JOIN statuses s ON i.status_id = s.status_id
            WHERE item_id = {item_id}
        ''')
        row = cursor.fetchone()
        return ItemModel.from_row(row) if row else None


def add_item(item: ItemModel) -> ItemModel:
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(
            'INSERT INTO items (name, brand, model, serial, location_id, status_id) VALUES (%s, %s, %s, %s, %s, %s)',
            (item.name, item.brand, item.model, item.serial, item.location_id, item.status_id)
        )
        item_id = cursor.lastrowid
    db.commit()
    return ItemModel(item_id=item_id, name=item.name, brand=item.brand, model=item.model,
                     serial=item.serial, location_id=item.location_id, status_id=item.status_id)


def update_item(item: ItemModel):
    db = get_db()
    with db.cursor() as cursor:
        query = 'UPDATE items SET'
        updates = []
        params = []

        if item.name is not None:
            updates.append(' name = %s')
            params.append(item.name)

        if item.brand is not None:
            updates.append(' brand = %s')
            params.append(item.brand)

        if item.model is not None:
            updates.append(' model = %s')
            params.append(item.model)

        if item.serial is not None:
            updates.append(' serial = %s')
            params.append(item.serial)

        if item.location_id is not None:
            updates.append(' location_id = %s')
            params.append(item.location_id)

        if item.status_id is not None:
            updates.append(' status_id = %s')
            params.append(item.status_id)

        if updates:
            query += ','.join(updates) + ' WHERE item_id = %s'
            params.append(item.item_id)
            cursor.execute(query, tuple(params))
            db.commit()


def delete_item(item_id: int):
    db = get_db()

    with db.cursor() as cursor:
        cursor.execute(f'DELETE FROM items WHERE item_id = {item_id}')
    db.commit()


def get_items_by_filters(brand=None, model=None, serial=None):
    db = get_db()
    query = '''
        SELECT i.item_id, i.name, i.brand, i.model, i.serial, i.location_id, l.name, i.status_id, s.name
        FROM items i 
        LEFT JOIN locations l ON i.location_id = l.location_id
        LEFT JOIN statuses s ON i.status_id = s.status_id
        WHERE 1=1'''
    values = []

    if brand:
        query += " AND brand LIKE ?"
        values.append(f"%{brand}%")
    if model:
        query += " AND model = ?"
        values.append(model)
    if serial:
        query += " AND serial = ?"
        values.append(serial)

    with db.cursor() as cursor:
        cursor.execute(query, tuple(values))
        item_tuples = cursor.fetchall()

    return ItemModel.list_from_rows(item_tuples)
