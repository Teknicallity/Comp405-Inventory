from flask import jsonify, request, redirect, url_for
from flask_login import login_required, current_user

from . import api
from db.models import checkout_model
from db.models.checkout_model import CheckoutModel
from db.models.user_model import User


@api.route('/checkouts/')
def all_checkouts():
    checkouts = checkout_model.get_all_checkouts()
    return jsonify(list(map((lambda checkout: checkout.to_dict()), checkouts))), 200


@api.route('/checkouts/', methods=['POST'])
@login_required
def create_checkout():
    user: User = current_user
    data = request.get_json()

    item_id = data.get('item_id')
    if user.is_admin:
        e_id = data.get('employee_id')
        employee_id = e_id if e_id not in (None, "") else user.employee_id
    else:
        employee_id = user.employee_id
    checkout = CheckoutModel(item_id=item_id, employee_id=employee_id)
    new_checkout = checkout_model.create_checkout(checkout)

    return jsonify(new_checkout.to_dict()), 200


@api.route('/checkouts/<int:checkout_id>/', methods=['GET'])
def get_checkout(checkout_id):
    checkout = checkout_model.get_checkout_by_id(checkout_id)
    if not checkout:
        return jsonify({'error': 'Checkout not found'}), 404
    return jsonify(checkout.to_dict()), 200


@api.route('/checkouts/<int:checkout_id>/', methods=['PUT'])
@login_required
def update_checkout(checkout_id):
    user: User = current_user
    checkout = checkout_model.get_checkout_by_id(checkout_id)

    if not user.is_admin and user.employee_id != checkout.employee_id:
        return jsonify({'error': 'Only an admin or checkout owner can update checkout'}), 403

    data = request.get_json()
    fields_to_update = {
        'item_id': data.get('item_id'),
        'employee_id': data.get('employee_id'),
    }

    for field, value in fields_to_update.items():
        if value not in (None, ""):
            setattr(checkout, field, value)

    checkout_model.update_checkout(checkout)
    return jsonify(checkout.to_dict()), 200


@api.route('/checkouts/<int:checkout_id>/return', methods=['POST'])
@login_required
def return_checkout(checkout_id):
    user: User = current_user
    checkout = checkout_model.get_checkout_by_id(checkout_id)
    if not checkout:
        return jsonify({'error': 'Checkout not found'}), 404

    if user.employee_id != checkout.employee_id and not user.is_admin:
        return jsonify({'error': 'Only the assigned employee or an admin can return checkout'}), 403

    next = request.args.get('next')
    returned_checkout = checkout_model.return_checkout(checkout_id)
    return redirect(next or url_for('main.checkout_details', checkout_id=checkout_id))


@api.route('/checkouts/<int:checkout_id>/', methods=['DELETE'])
@login_required
def delete_checkout(checkout_id):
    user: User = current_user
    if not user.is_admin:
        return jsonify({'error': 'Only an admin can delete checkout'}), 403
    next = request.args.get('next')
    checkout = checkout_model.get_checkout_by_id(checkout_id)

    checkout_model.delete_checkout(checkout_id)
    return jsonify({
        'message': 'Checkout deleted successfully',
        'next_url': next or url_for('main.all_checkouts')
    })
