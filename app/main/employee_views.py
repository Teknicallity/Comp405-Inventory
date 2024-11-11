from flask_login import login_required, current_user
from flask import render_template, abort

from app.main import main
from db.models.employee_model import get_all_employees, get_employee_by_id
from db.models.user_model import User


@main.route('/employees/')
@login_required
def all_employees():
    user: User = current_user
    if not user.is_admin:
        return abort(403)
    employees = get_all_employees()
    return render_template('employee_list.html', employees=employees)


@main.route('/employees/<int:employee_id>')
@login_required
def employee_details(employee_id):
    user: User = current_user
    if not user.is_admin:
        return abort(403)
    employee = get_employee_by_id(employee_id)
    return render_template('employee.html', employee=employee)


@main.route('/employees/create/')
@login_required
def create_employee():
    user: User = current_user
    if not user.is_admin:
        return abort(403)
    return render_template('employee.html')
