from app.main import main
from db.models.item_model import get_all_items, get_item_by_id
from flask import jsonify, render_template


@main.route('/')
def index():
    return render_template('home.html')


@main.route('/inventory/items')
def inventory():
    items = get_all_items()
    return render_template('inventory_items.html', items=items)


@main.route('/inventory/items/<int:item_id>')
def inventory_item(item_id):
    item = get_item_by_id(item_id)
    return render_template('item.html', item=item)
