from flask import jsonify, request, redirect, url_for
from flask_login import login_required, current_user

from db.models.user_model import User
from . import api
from db.models import documentation_model
from db.models.documentation_model import DocumentationModel


@api.route('/documentation/')
def all_documentation():
    documentation = documentation_model.get_all_documentation()
    return jsonify(list(map((lambda document: document.to_dict()), documentation))), 200


@api.route('/documentation/', methods=['POST'])
@login_required
def create_documentation():
    user: User = current_user
    data: dict = request.get_json()

    url = data.get('url')
    description = data.get('description')
    item_id = data.get('item_id')

    if not (url and description and item_id):
        return jsonify({'error': 'Missing data'}), 400

    documentation = DocumentationModel(
        url=url,
        description=description,
        item_id=item_id
    )
    new_documentation = documentation_model.add_documentation(documentation)
    return jsonify(new_documentation.to_dict()), 201

@api.route('/documentation/<int:documentation_id/', methods=['GET'])
def get_documentation_by_id(documentation_id):
    documentation = documentation_model.get_documentation_by_id(documentation_id)
    if not documentation:
        return jsonify({'error': 'Document not found'}), 404
    return jsonify(documentation.to_dict()), 200


@api.route('/documentation/<int:documentation_id>/', methods=['PUT'])
@login_required
def update_documentation(documentation_id):
    documentation = documentation_model.get_documentation_by_id(documentation_id)
    if not documentation:
        return jsonify({'error': 'Document not found'}), 404

    data = request.get_json()
    fields_to_update = {
        'url': data.get('url'),
        'description': data.get('description'),
        'item_id': data.get('item_id')
    }

    for field, value in fields_to_update.items():
        if value not in (None, ""):
            setattr(documentation, field, value)

    documentation_model.update_documentation(documentation)
    return jsonify(documentation.to_dict()), 200


@api.route('/documentation/<int:documentation_id>/', methods=['DELETE'])
@login_required
def delete_documentation(documentation_id):
    documentation = documentation_model.get_documentation_by_id(documentation_id)
    if not documentation:
        return jsonify({'error': 'Document not found'}), 404

    next = request.args.get('next')

    documentation_model.delete_documentation(documentation_id)
    return jsonify({
        'message': 'Document deleted successfully',
        'next_url': next or url_for('main.all_documentation')
    }), 200
