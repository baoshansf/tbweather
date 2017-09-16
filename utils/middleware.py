# -*- coding: utf-8 -*-
import time
from django.utils.deprecation import MiddlewareMixin
from loger import _access_log

class LogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        setattr(request, 'start_time', time.time())
        return None

    def process_response(self, request, response):
        status_code = response.status_code
        if status_code < 400:
            log_method = _access_log.info
        elif status_code < 500:
            log_method = _access_log.warning
        else:
            log_method = _access_log.error

        request_time = int(1000 * (time.time() - request.start_time))
        try:
            remote_ip = request.META['HTTP_X_FORWARDED_FOR'].split(',')[0]
        except Exception as e:
            remote_ip = request.META['REMOTE_ADDR']
        request_url = request.path_info
        method = request.method
        if method == 'GET' and request.GET:
            params_list = list()
            for key in request.GET:
                params_list.append(key + '=' + request.GET[key])
            request_url += '?' + '&'.join(params_list)
        log_method("%s %sms %s %s %s" % (str(status_code), str(request_time), method, request_url, remote_ip))
        return response