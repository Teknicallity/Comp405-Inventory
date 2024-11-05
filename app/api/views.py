from . import api


@api.route('/')
def hello():
    return {'message': 'Hello World!'}
