from collections import OrderedDict

from flask import Flask
from werkzeug.wsgi import DispatcherMiddleware

import config
from ext import sse
from views import home, json_api


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    app.register_blueprint(home.bp)
    app.register_blueprint(sse, url_prefix='/stream')
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, OrderedDict((
        ('/j', json_api),
    )))
    return app


app = create_app()

# For local test
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8100, debug=app.debug)
