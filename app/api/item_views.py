from flask import jsonify, request, render_template, url_for, redirect
from flask_login import login_required

from db.models.item_model import ItemModel, add_item
from . import api
from db.models import item_model
from .forms import CreateItemForm, UpdateItemForm, DeleteItemForm
from .. import debug_only


@api.route('/items/')
def all_items():
    items = item_model.get_all_items()
    return jsonify(list(map((lambda item: item.to_dict()), items))), 200


@api.route('/items/<int:item_id>', methods=['GET'])
def get_single_item(item_id):
    item = item_model.get_item_by_id(item_id)
    if item:
        return jsonify(item.to_dict()), 200
    else:
        return jsonify({"error": "Item not found"}), 404


@api.route('/items/', methods=['POST'])
@login_required
def create_item():
    data = request.get_json()

    name = data.get('name')
    if not name:
        return jsonify({"error": "The 'name' field is required"}), 400

    brand = data.get('brand') or None
    model = data.get('model') or None
    serial = data.get('serial') or None

    item = ItemModel(name, brand, model, serial)
    new_item = add_item(item)

    return jsonify(new_item.to_dict()), 201


@api.route('/items/<int:item_id>', methods=['PUT'])
@login_required
def update_item(item_id):
    item = item_model.get_item_by_id(item_id)
    if not item:
        return jsonify({"error": f"Item with ID {item_id} not found"}), 404

    data = request.get_json()
    fields_to_update = {
        "name": data.get("name"),
        "brand": data.get("brand"),
        "model": data.get("model"),
        "serial": data.get("serial"),
        "location_id": data.get("location_id"),
        "status_id": data.get("status_id"),
    }

    for field, value in fields_to_update.items():
        if value not in (None, ""):
            setattr(item, field, value)

    item_model.update_item(item)

    return jsonify(item.to_dict()), 200


@api.route('/items/<int:item_id>', methods=['DELETE'])
@login_required
def delete_item(item_id):
    item = item_model.get_item_by_id(item_id)
    next = request.args.get('next')
    if not item:
        return jsonify({"error": "Item not found"}), 404

    item_model.delete_item(item.item_id)
    return redirect(next or url_for('main.all_items'))


@api.route('/itemtest/', methods=['GET'])
@debug_only
def all_test():
    create_form = CreateItemForm()
    update_form = UpdateItemForm()
    delete_form = DeleteItemForm()

    return render_template(
        'example_requests.html',
        create_form=create_form,
        update_form=update_form,
        delete_form=delete_form
    )
