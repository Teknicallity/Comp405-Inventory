from flask import current_app, g
def get_db():
    if 'db' not in g:
        g.db =