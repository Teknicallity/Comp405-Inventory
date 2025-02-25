from flask_login import login_required, current_user
from flask import render_template, abort, request

from app.main import main
from db.models.employee_model import get_all_employees, get_employee_by_id, get_employees_by_reports_to
from db.models.user_model import User


@main.route('/employees/')
@login_required
def all_employees():
    user: User = current_user

    employees = get_all_employees()
    return render_template('employee_list.html', employees=employees)


@main.route('/employees/<int:employee_id>')
@login_required
def employee_details(employee_id):
    if employee_id == 0:
        return 'user does not have employee id'
    user: User = current_user
    if not (user.is_admin or user.employee_id == employee_id):
        return abort(403)
    employee = get_employee_by_id(employee_id)
    if employee is None:
        return abort(404)
    possible_managers = get_all_employees()
    return render_template('employee.html', employee=employee, reports_to_choices=possible_managers)


@main.route('/employees/create/')
@login_required
def create_employee():
    user: User = current_user
    if not user.is_admin:
        return abort(403)
    possible_managers = get_all_employees()
    return render_template('employee.html', reports_to_choices=possible_managers)


@main.route('/employees/filter/')
@login_required
def filter_employees():
    user: User = current_user

    filter_type = request.args.get('filter', 'reports')

    if filter_type == 'leads':
        employees = get_employees_by_reports_to(None)
    else:
        employees = get_employees_by_reports_to(not None)

    return render_template('home.html', employees=employees)