# coding=utf-8


import json

import requests
from django.http import HttpResponse
from requests.exceptions import ReadTimeout
# from utils.loger import code_log, sentry_log

from utils.tools import retry


class ApiResponse(object):
    """
    所有api返回遵从此基本结构
    """
    @staticmethod
    def failure(code, msg):
        data = {
            "code": code,
            "msg": msg,
            "data": None
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    @staticmethod
    def success(data=None):
        data = {
            "code": 0,
            "msg": "",
            "data": data
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

#
# class RetryRequests(object):
#     """
#     封装在requests基础上加上重试机制
#     """
#     @staticmethod
#     @retry([ReadTimeout], try_times=2, delay=1, logger=code_log, sentry_log=sentry_log)
#     def get(*args, **kwargs):
#         return requests.get(*args, **kwargs)
#
#     @staticmethod
#     @retry([ReadTimeout], try_times=2, delay=1, logger=code_log, sentry_log=sentry_log)
#     def post(*args, **kwargs):
#         return requests.post(*args, **kwargs)
#
#     @staticmethod
#     @retry([ReadTimeout], try_times=2, delay=1, logger=code_log, sentry_log=sentry_log)
#     def delete(*args, **kwargs):
#         return requests.post(*args, **kwargs)
#
#     @staticmethod
#     @retry([ReadTimeout], try_times=2, delay=1, logger=code_log, sentry_log=sentry_log)
#     def put(*args, **kwargs):
#         return requests.post(*args, **kwargs)
