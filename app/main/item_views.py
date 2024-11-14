from flask_login import login_required, current_user
from flask import render_template, abort

from app.main import main
from db.models.item_model import get_all_items, get_item_by_id
from db.models.location_model import get_all_locations
from db.models.status_model import get_all_statuses
from db.models.user_model import User


@main.route('/inventory/items/')
def all_items():
    items = get_all_items()
    return render_template('item_list.html', items=items)


@main.route('/inventory/items/<int:item_id>')
def item_details(item_id):
    item = get_item_by_id(item_id)
    if item is None:
        abort(404)
    locations = get_all_locations()
    statuses = get_all_statuses()
    return render_template('item.html', item=item, locations=locations, statuses=statuses)


@main.route('/inventory/items/create')
@login_required
def create_item():
    locations = get_all_locations()
    statuses = get_all_statuses()
    return render_template('item.html', locations=locations, statuses=statuses)
