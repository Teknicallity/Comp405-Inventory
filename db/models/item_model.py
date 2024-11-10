from flask import abort

from db.connection import get_db


class ItemModel:
    def __init__(self, name, brand=None, model=None, serial=None, item_id=None):
        self.name = name
        self.brand = brand
        self.model = model
        self.serial = serial
        self.item_id = item_id

    @classmethod
    def from_row(cls, row):
        return cls(
            name=row[1],
            brand=row[2],
            model=row[3],
            serial=row[4],
            item_id=row[0]
        )

    @classmethod
    def list_from_rows(cls, rows) -> list:
        item_list = []
        for item in rows:
            item_list.append(ItemModel.from_row(item))
        return item_list

    def to_dict(self):
        # Convert the object attributes to a dictionary
        return {
            "item_id": self.item_id,
            "name": self.name,
            "brand": self.brand,
            "model": self.model,
            "serial": self.serial
        }


def get_all_items():
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute('SELECT * FROM items')
        return ItemModel.list_from_rows(cursor.fetchall())


def get_item_by_id(item_id: int):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(f'SELECT * FROM items WHERE item_id = {item_id}')
        row = cursor.fetchone()
        return ItemModel.from_row(row) if row else None


def add_item(item: ItemModel) -> ItemModel:
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(
            'INSERT INTO items (name, brand, model, serial) VALUES (%s, %s, %s, %s)',
            (item.name, item.brand, item.model, item.serial)
        )
        item_id = cursor.lastrowid
    db.commit()
    return ItemModel(item_id=item_id, name=item.name, brand=item.brand, model=item.model,
                     serial=item.serial)


def update_item(item: ItemModel):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(f'''
            UPDATE items
            SET name = %s, brand = %s, model = %s, serial = %s
            WHERE item_id = %s
        ''', (item.name, item.brand, item.model, item.serial, item.item_id))
    db.commit()


def delete_item(item_id: int):
    db = get_db()

    with db.cursor() as cursor:
        cursor.execute(f'DELETE FROM items WHERE item_id = {item_id}')
    db.commit()


def get_items_by_filters(brand=None, model=None, serial=None):
    db = get_db()
    query = "SELECT * FROM items WHERE 1=1"
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
