from app.main import main
from db.models.item_model import get_all_items
from flask import jsonify

@main.route('/')
def index():
    return 'Hello World!'

@main.route('/items')
def all_items():
    items = get_all_items()
    return jsonify(items)
