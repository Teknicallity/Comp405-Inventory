from app.main import main
from db.models.item_model import get_all_items
from flask import jsonify, render_template


@main.route('/')
def index():
    return render_template('home.html')


@main.route('/items')
def all_items():
    items = get_all_items()
    return jsonify(items)
