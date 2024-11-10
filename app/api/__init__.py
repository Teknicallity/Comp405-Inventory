from flask import Blueprint

api = Blueprint('api', __name__)
from . import views
from . import item_views
from . import employee_view