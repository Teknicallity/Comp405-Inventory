from app.main import main
from db.flask_setup import get_db
from flask import jsonify

@main.route('/')
def index():
    return 'Hello World!'

@main.route('/items')
def about():
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
    print(items)
    return jsonify(items)