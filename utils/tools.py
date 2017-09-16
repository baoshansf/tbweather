# coding=utf-8

import time
import functools


class TimeCounter(object):
    """
    用于统计某一块、几行或某一个函数的执行时长
    """
    def __init__(self, msg, logger, console=False):
        self.msg = msg
        self.logger = logger
        self.console = console

    def __enter__(self):
        self.begin = time.clock()

    def __exit__(self, e_t, _e_v, t_b):
        self.end = time.clock()
        success = "false" if e_t else "true"
        self.logger.info("[%s] cost:%.4fs success:%s" % (self.msg, self.end - self.begin, success))
        if self.console:
            print "[%s] cost:%.4fs success:%s" % (self.msg, self.end - self.begin, success)

    @staticmethod
    def time_count(tag, logger, console=False):
        """
        用于函数统计
        """
        def _time_count(func):
            @functools.wraps(func)
            def _wrapper(*args, **kwargs):
                begin = time.clock()
                success = "true"
                try:
                    return func(*args, **kwargs)
                except:
                    success = "false"
                    raise
                finally:
                    end = time.clock()
                    logger.info("[%s] cost:%.4fs success:%s" % (tag, end - begin, success))
                    if console:
                        print "[%s] cost:%.4fs success:%s" % (tag, end - begin, success)
            return _wrapper
        return _time_count


def retry(exc_cls_list, try_times=2, delay=0, logger=None, sentry_log=None):
    """
    重试装饰器
    当被装饰的函数运行发生exc_cls_list中的某一个异常时会进行重试
    最多重试try_times次
    Args:
        exc_cls_list: 异常类列表
        try_times: 重试次数
        delay: 重试延时
        logger: 日志对象
        sentry_log: sentry网络日志

    Returns:

    """
    def deco_retry(func):
        def _retry(*args, **kwargs):
            _retry_time = try_times
            while _retry_time > 0:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if any([isinstance(e, exc) for exc in exc_cls_list]):
                        msg = "%s, retrying in %d seconds..." % (str(e), delay)
                        if logger:
                            logger.warning(msg)
                        if delay > 0:
                            time.sleep(delay)
                    else:
                        if sentry_log:
                            sentry_log.captureException()
                _retry_time -= 1
            return func(*args, **kwargs)
        return _retry
    return deco_retry
