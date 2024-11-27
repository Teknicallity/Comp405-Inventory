from flask import render_template, abort
from flask_login import login_required, current_user

from app.main import main
from app.main.employee_views import all_employees
from db.models import checkout_model
from db.models.employee_model import get_all_employees
from db.models.item_model import get_all_items

from db.models.user_model import User


@main.route('/checkouts/')
@login_required
def all_checkouts():
    # user: User = current_user
    checkouts = checkout_model.get_all_checkouts()
    return render_template('checkout_list.html', checkouts=checkouts)


@main.route('/checkouts/<int:checkout_id>/')
@login_required
def checkout_details(checkout_id):
    # user: User = current_user
    checkout = checkout_model.get_checkout_by_id(checkout_id)
    if checkout is None:
        abort(404)
    all_items = get_all_items()
    employees = get_all_employees()
    return render_template(
        'checkout.html',
        checkout=checkout,
        item_choices=all_items,
        employee_choices=employees
    )


@main.route('/checkouts/create/')
@login_required
def create_checkout():
    all_items = get_all_items()
    employees = get_all_employees()
    return render_template(
        'checkout.html',
        item_choices=all_items,
        employee_choices=employees
    )
