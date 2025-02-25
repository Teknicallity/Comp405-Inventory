from db.connection import get_db


class DocumentationModel:
    def __init__(self, documentation_id=None, url=None, description=None, item_id=None, item_name=None):
        self.documentation_id = documentation_id
        self.url = url
        self.description = description
        self.item_id = item_id
        self.item_name = item_name

    @classmethod
    def from_row(cls, row):
        return cls(
            documentation_id=row[0],
            url=row[1],
            description=row[2],
            item_id=row[3],
            item_name=row[4],
        )

    @classmethod
    def list_from_rows(cls, rows):
        return [cls.from_row(row) for row in rows]

    def to_dict(self):
        return {
            'checkout_id': self.documentation_id,
            'url': self.url,
            'description': self.description,
            'item_id': self.item_id,
            'item_name': self.item_name,
        }


def get_all_documentation():
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute('''
            SELECT d.documentation_id, d.url, d.description, d.item_id, i.name
            FROM documentation d
            LEFT JOIN items i ON d.item_id = i.item_id
        ''')
        return DocumentationModel.list_from_rows(cursor.fetchall())


def add_documentation(documentation: DocumentationModel):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(
            'INSERT INTO documentation (url, description, item_id) VALUES (%s, %s, %s)',
            (documentation.url, documentation.description, documentation.item_id)
        )
        documentation_id = cursor.lastrowid
    db.commit()

    return DocumentationModel(
        documentation_id=documentation_id,
        url=documentation.url,
        description=documentation.description,
        item_id=documentation.item_id
    )


def get_documentation_by_id(document_id: int) -> DocumentationModel:
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute('''
            SELECT d.documentation_id, d.url, d.description, d.item_id, i.name
            FROM documentation d
            LEFT JOIN items i ON d.item_id = i.item_id
            WHERE d.documentation_id = %s
        ''', (document_id,))
        row = cursor.fetchone()

        return DocumentationModel.from_row(row) if row else None


def get_documentation_for_item_id(item_id: int) -> list[DocumentationModel]:
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute('''
            SELECT d.documentation_id, d.url, d.description, d.item_id, i.name
            FROM documentation d
            LEFT JOIN items i ON d.item_id = i.item_id
            Where d.item_id = %s
        ''', (item_id,))
        rows = cursor.fetchall()

        return DocumentationModel.list_from_rows(rows) if len(rows) > 0 else None


def update_documentation(documentation: DocumentationModel):
    db = get_db()
    with db.cursor() as cursor:
        query = 'UPDATE documentation SET'
        updates = []
        params = []

        if documentation.url is not None:
            updates.append(' url = %s')
            params.append(documentation.url)

        if documentation.description is not None:
            updates.append(' description = %s')
            params.append(documentation.description)

        if documentation.item_id is not None:
            updates.append(' item_id = %s')
            params.append(documentation.item_id)

        if updates:
            query += ','.join(updates) + ' WHERE documentation_id = %s'
            params.append(documentation.documentation_id)
            cursor.execute(query, tuple(params))
            db.commit()


def delete_documentation(document_id: int):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute('DELETE FROM documentation WHERE documentation_id = %s', (document_id,))
        db.commit()