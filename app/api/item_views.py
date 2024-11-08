from flask import jsonify, request

from . import api
from db.models import item_model


@api.route('/items')
def all_items():
    items = item_model.get_all_items()
    return jsonify(items.to_dict()), 200


@api.route('/items/<int:item_id>', methods=['GET'])
def get_single_item(item_id):
    item = item_model.get_item_by_id(item_id)
    if item:
        return jsonify(item.to_dict()), 200
    else:
        return jsonify({"error": "Item not found"}), 404


@api.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = item_model.get_item_by_id(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json()

    name = data.get('name', item.name)
    brand = data.get('brand', item.brand)
    model_number = data.get('model_number', item.model_number)
    serial_number = data.get('serial_number', item.serial_number)

    item.name = name
    item.brand = brand
    item.model_number = model_number
    item.serial_number = serial_number

    item_model.update_item(item)

    return jsonify(item.to_dict()), 200
