from flask import jsonify, abort, request, redirect, url_for
from flask_login import login_required, current_user

from db.models.employee_model import EmployeeModel
from db.models.user_model import User
from . import api
from db.models import employee_model


@api.route('/employees/')
@login_required
def all_employees():
    employees = employee_model.get_all_employees()
    return jsonify(list(map((lambda employee: employee.to_dict()), employees))), 200


@api.route('/employees/', methods=['POST'])
@login_required
def create_employee():
    user: User = current_user
    if not user.is_admin:
        return abort(401)

    data: dict = request.get_json()
    first_name = data.get('first_name') or None
    last_name = data.get('last_name') or None
    title = data.get('title') or None
    reports_to_id = data.get('reports_to') or None
    username = data.get('username') or None
    password = data.get('password') or None
    is_admin = True if data.get('is_admin') is True else False

    if not (first_name and last_name and title):
        return abort(400)

    employee = EmployeeModel(
        first_name=first_name,
        last_name=last_name,
        title=title,
        reports_to=reports_to_id,
        username=username,
        password=password,
        is_admin=is_admin
    )
    try:
        new_employee = employee_model.add_employee(employee)
    except ValueError:
        return abort(422)

    return jsonify(new_employee.to_dict()), 201


@api.route('/employees/<int:employee_id>/', methods=['GET'])
@login_required
def get_employee(employee_id):
    employee = employee_model.get_employee_by_id(employee_id)
    if employee:
        return jsonify(employee.to_dict()), 200
    else:
        return jsonify({'message': 'Employee not found'}), 404


@api.route('/employees/<int:employee_id>/', methods=['PUT'])
@login_required
def update_employee(employee_id):
    user: User = current_user
    if not (user.is_admin or user.employee_id == employee_id):
        return abort(401)

    employee = employee_model.get_employee_by_id(employee_id)
    if not employee:
        return jsonify({'message': 'Employee not found'}), 404

    data = request.get_json()
    fields_to_update = {}
    if user.is_admin:
        fields_to_update = {
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'title': data.get('title'),
            'reports_to': data.get('reports_to'),
            'username': data.get('username'),
            'password': data.get('password'),
            'is_admin': True if data.get('is_admin') is True else False
        }
    elif user.employee_id == employee_id:
        fields_to_update = {
            'username': data.get('username'),
            'password': data.get('password'),
        }

    for field, value in fields_to_update.items():
        if value not in (None, ""):
            setattr(employee, field, value)

    employee_model.update_employee(employee)

    return jsonify(employee.to_dict()), 200


@api.route('/employees/<int:employee_id>/', methods=['DELETE'])
@login_required
def delete_employee(employee_id):
    user: User = current_user
    if not user.is_admin:
        return abort(401)

    employee = employee_model.get_employee_by_id(employee_id)
    next = request.args.get('next')
    if not employee:
        return jsonify({'message': 'Employee not found'}), 404

    employee_model.delete_employee(employee.employee_id)
    return jsonify({
        'message': 'Employee deleted successfully',
        'next_url': next or url_for('main.all_employees')
    }), 200


@api.route('/employees/filter/', methods=['GET'])
@login_required
def filter_employees():
    user: User = current_user
    
    filter_type = request.args.get('filter', None)

    if filter_type == 'leads':
        employees = employee_model.get_employees_by_reports_to(None)
    elif filter_type == 'reports':
        employees = employee_model.get_employees_by_reports_to(not None)
    elif filter_type is None:
        employees = employee_model.get_all_employees()
    else:
        return jsonify({'error': 'Invalid filter type'}), 400
    
    return jsonify(list(map((lambda employee: employee.to_dict()), employees))), 200
