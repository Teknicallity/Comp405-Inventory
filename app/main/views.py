from flask_login import login_required, current_user
from flask import jsonify, render_template, abort

from app import debug_only
from app.main import main
from db.models.checkout_model import get_all_checkouts
from db.models.employee_model import get_all_employees
from db.models.item_model import get_all_items
from db.models.user_model import User


@main.route('/')
def index():
    items = get_all_items()
    checkouts = get_all_checkouts()
    employees = get_all_employees()
    return render_template('home.html', items=items, checkouts=checkouts, employees=employees)
