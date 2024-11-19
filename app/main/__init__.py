from flask import Blueprint

main = Blueprint('main', __name__)
from . import views
from . import item_views
from . import employee_views
from . import checkout_views
from . import documentation_views
