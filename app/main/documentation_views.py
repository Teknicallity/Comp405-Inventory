from flask import render_template, abort
from flask_login import login_required, current_user

from app.main import main
from db.models import documentation_model
from db.models.item_model import get_all_items


@main.route('/documentation/')
@login_required
def all_documentation():
    # user: User = current_user
    documentation = documentation_model.get_all_documentation()
    return render_template('documentation_list.html', documentation=documentation)


@main.route('/documentation/<int:documentation_id>/')
def documentation_details(documentation_id):
    # user: User = current_user
    document = documentation_model.get_documentation_by_id(documentation_id)
    if document is None:
        abort(404)
    items = get_all_items()
    return render_template('documentation.html', document=document, items=items)


@main.route('/documentation/create/')
@login_required
def create_documentation():
    items = get_all_items()
    return render_template('documentation.html', items=items)
