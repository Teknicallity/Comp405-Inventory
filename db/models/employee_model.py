from db.connection import get_db
from db.models import user_model
from db.models.user_model import get_user_by_id, get_user_by_employee_id, update_user


class EmployeeModel:
    def __init__(self, first_name, last_name, title, reports_to=None, employee_id=None, reports_to_name=None,
                 username=None, password=None, is_admin=False):
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.title = title
        self.reports_to = reports_to
        self.reports_to_name = reports_to_name
        self.username = username
        self.password = password
        self.is_admin = is_admin

    @classmethod
    def from_row(cls, row):
        return cls(
            employee_id=row[0],
            first_name=row[1],
            last_name=row[2],
            title=row[3],
            reports_to=row[4],
            reports_to_name=row[5] or None,
            username=row[6],
            is_admin=row[7]
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
            'reports_to_name': self.reports_to_name,
            'username': self.username,
            'is_admin': self.is_admin
        }


def get_all_employees() -> list:
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute('''
            SELECT e.employee_id, e.first_name, e.last_name, e.title, e.reports_to,
                   CONCAT(r.first_name, ' ', r.last_name), u.username, u.is_admin
            FROM employees e
            LEFT JOIN employees r ON e.reports_to = r.employee_id
            LEFT JOIN users u ON e.employee_id = u.employee_id
        ''')
        return EmployeeModel.list_from_row(cursor.fetchall())


def get_employee_by_id(employee_id: int) -> EmployeeModel:
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(f'''
            SELECT e.employee_id, e.first_name, e.last_name, e.title, e.reports_to,
                   CONCAT(r.first_name, ' ', r.last_name), u.username, u.is_admin
            FROM employees e
            LEFT JOIN employees r ON e.reports_to = r.employee_id
            LEFT JOIN users u ON e.employee_id = u.employee_id
            WHERE e.employee_id={employee_id}
        ''')
        row = cursor.fetchone()
        return EmployeeModel.from_row(row) if row else None


def add_employee(employee: EmployeeModel) -> EmployeeModel:
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute('''
            INSERT INTO employees (first_name, last_name, title, reports_to)
            VALUES (%s, %s, %s, %s)
            ''', (employee.first_name, employee.last_name, employee.title, employee.reports_to)
        )
        employee_id = cursor.lastrowid
    db.commit()

    if employee.username:
        user_model.add_user(
            username=employee.username,
            password=employee.password,
            employee_id=employee_id,
            is_admin=employee.is_admin
        )
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

        if employee.is_admin is not None or employee.username or employee.password:
            update_user(
                employee_id=employee.employee_id,
                is_admin=employee.is_admin,
                username=employee.username,
                password=employee.password,
            )
    db.commit()


def delete_employee(employee_id: int):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(f'DELETE FROM employees WHERE employee_id={employee_id}')
    db.commit()
