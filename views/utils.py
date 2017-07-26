from datetime import datetime
from flask import json
from werkzeug.wrappers import Response


class DateTimeEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, bytes):
            return o.decode('utf-8')

        return json.JSONEncoder.default(self, o)


class ApiResult(object):

    def __init__(self, value, status=200):
        self.value = value
        self.status = status

    def to_response(self):
        return Response(json.dumps(self.value, cls=DateTimeEncoder),
                        status=self.status,
                        mimetype='application/json')
