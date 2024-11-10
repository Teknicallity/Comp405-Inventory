from flask_login import login_required, current_user

from app.main import main
from db.models.employee_model import get_all_employees, get_employee_by_id
from db.models.item_model import get_all_items, get_item_by_id
from flask import jsonify, render_template, abort

from db.models.user_model import User


@main.route('/')
def index():
    return render_template('home.html')


@main.route('/inventory/items/')
def inventory():
    items = get_all_items()
    return render_template('inventory_items.html', items=items)


@main.route('/inventory/items/<int:item_id>')
def inventory_item(item_id):
    item = get_item_by_id(item_id)
    return render_template('item.html', item=item)


@main.route('/employees/')
@login_required
def all_employees():
    user: User = current_user
    if not user.is_admin:
        return abort(401)
    employees = get_all_employees()
    print(employees[0].to_dict())
    return render_template('employee_list.html', employees=employees)


@main.route('/employees/<int:employee_id>')
@login_required
def employee_detail(employee_id):
    user: User = current_user
    if not user.is_admin:
        return abort(401)
    employee = get_employee_by_id(employee_id)
    return render_template('employee.html', employee=employee)
