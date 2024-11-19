from flask import Blueprint

api = Blueprint('api', __name__)
from . import views
from . import item_views
from . import employee_view
from . import checkout_views
from . import documentation_views
