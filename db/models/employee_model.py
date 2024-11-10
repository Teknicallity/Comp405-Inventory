from db.connection import get_db


class EmployeeModel:
    def __init__(self, first_name, last_name, title, reports_to=None, employee_id=None):
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.title = title
        self.reports_to = reports_to

    @classmethod
    def from_row(cls, row):
        return cls(
            employee_id=row[0],
            first_name=row[1],
            last_name=row[2],
            title=row[3],
            reports_to=row[4],
        )

    @classmethod
    def list_from_row(cls, rows) -> list:
        return [cls.from_row(row) for row in rows]

    def to_dict(self):
        return {
            'employee_id': self.employee_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'title': self.title,
            'reports_to': self.reports_to,
        }


def get_all_employees() -> list:
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute('SELECT * FROM employees')
        return EmployeeModel.list_from_row(cursor.fetchall())


def get_employee_by_id(employee_id: int) -> EmployeeModel:
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(f'SELECT * FROM employees WHERE employee_id={employee_id}')
        row = cursor.fetchone()
        return EmployeeModel.from_row(row) if row else None


def add_employee(employee: EmployeeModel) -> EmployeeModel:
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(
            'INSERT INTO employees (first_name, last_name, title, reports_to) VALUES (%s, %s, %s, %s)',
            (employee.first_name, employee.last_name, employee.title, employee.reports_to)
        )
        employee_id = cursor.lastrowid
    db.commit()
    return EmployeeModel(
        employee_id=employee_id,
        first_name=employee.first_name,
        last_name=employee.last_name,
        title=employee.title,
        reports_to=employee.reports_to,
    )


def update_employee(employee: EmployeeModel):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(f'''
            UPDATE employees
            SET first_name=%s, last_name=%s, title=%s, reports_to=%s
            WHERE employee_id=%s
        ''', (employee.first_name, employee.last_name, employee.title, employee.reports_to, employee.employee_id))
    db.commit()


def delete_employee(employee_id: int):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(f'DELETE FROM employees WHERE employee_id={employee_id}')
    db.commit()
