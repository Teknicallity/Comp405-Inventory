from flask import render_template, abort
from flask_login import login_required, current_user

from app.main import main
from db.models import documentation_model


@main.route('/documentation/')
@login_required
def all_documentation():
    # user: User = current_user
    documentation = documentation_model.get_all_documentation()
    return render_template('documenation_list.html', documentation=documentation)


@main.route('/documentation/<int:document_id>/')
def documentation_details(document_id):
    # user: User = current_user
    document = documentation_model.get_documentation_by_id(document_id)
    if document is None:
        abort(404)
    return render_template('documenation.html', document=document)


@main.route('/documentation/create/')
@login_required
def create_documentation():
    return render_template('documenation.html')
