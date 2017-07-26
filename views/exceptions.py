# coding=utf-8
from views.utils import ApiResult


class ApiException(Exception):

    def __init__(self, error, real_message=None):
        self.code, self.message, self.status = error
        if real_message is not None:
            self.message = real_message

    def to_result(self):
        return ApiResult({'msg': self.message, 'r': self.code},
                         status=self.status)
