# # coding=utf-8
#
# """
# 程序运行日志记录
# """
#
# import logging
# import os
# from cloghandler import ConcurrentRotatingFileHandler as LogHandler
# import platform
# from raven import Client
#
#
# if str(platform.system()) == "Windows":
#     from logging.handlers import RotatingFileHandler as LogHandler
#
# _log_file_size = 1 * 1024 * 1024 * 1024  # 1G
#
# _log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
#                          "logs")
#
# # -------------------------------运行日志（代码运行记录）-------------------------------
# _code_log_file = os.path.join(_log_path, 'code.log')
# _code_log_handler = LogHandler(_code_log_file, "a", _log_file_size, 1000)
# _code_log_formatter = logging.Formatter('%(levelname)s %(asctime)s %(pathname)s %(funcName)s '
#                                         'line:%(lineno)d %(message)s')
# _code_log_handler.setFormatter(_code_log_formatter)
# # 此处设置logger名称，否则默认的会和tornado的logger相同而使得下方设置的错误等级被更新为info
# code_log = logging.getLogger('code-log')
# code_log.setLevel(logging.INFO)
# code_log.addHandler(_code_log_handler)
#
# # -------------------------------Sentry网络日志系统--------------------------------
# sentry_log = Client('http://726e52915d7440619fa765fbd27e7620:0a88f516340d41f3a8b2c3b28537221c@10.51.30.4/4')
#
# # -------------------------------访问日志（记录访问的url和body）----------------------------------------
# _access_log_file = os.path.join(_log_path, 'access.log')
# _access_log_handler = LogHandler(_access_log_file, "a", _log_file_size, 1000)
# _access_log_formatter = logging.Formatter('%(asctime)s:%(message)s')
# _access_log_handler.setFormatter(_access_log_formatter)
# _access_log = logging.getLogger('access-log')
# _access_log.setLevel(logging.INFO)
# _access_log.addHandler(_access_log_handler)
