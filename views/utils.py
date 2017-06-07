from datetime import datetime
from flask import json
from werkzeug.wrappers import Response


def datetime_handler(x):
    if isinstance(x, datetime):
        return x.isoformat()
    raise TypeError('Unknown type')


class ApiResult(object):
    def __init__(self, value, status=200):
        self.value = value
        self.status = status
    def to_response(self):
        return Response(json.dumps(self.value, default=datetime_handler),
                        status=self.status,
                        mimetype='application/json')
