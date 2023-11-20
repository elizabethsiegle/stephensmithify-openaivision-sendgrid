#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import datetime
import arrow


def timestamps():
    """
    返回当前整形的时间戳（UTC+8h）
    """
    return int(time.time())


def microtime():
    """
    返回当前的微妙级别的时间戳（UTC+8h）
    :return:
    """
    return time.time()


def time_format(timestamp=None, format="%Y-%m-%d %X"):
    """
    根据入参的时间戳和格式化一个时间戳(UTC+8h)
    """
    if timestamp is None:
        timestamp = int(time.time())

    struct_time = time.localtime(int(timestamp))
    return time.strftime(format, struct_time)


def time_now_format(format="%Y-%m-%d %X"):
    """
    格式化当前时间格式化一个时间戳(UTC+8h)
    """
    timestamp = int(time.time())
    struct_time = time.localtime(int(timestamp))
    return time.strftime(format, struct_time)


def strtotime(format_time):
    """
    时间格式转换成时间戳。
    支持两种时间格式：
    1、YYYY-MM-DD hh:mm:ss 
    2、YYYY/MM/DD hh:mm:ss
    """
    try:
        struct_time = time.strptime(format_time, "%Y/%m/%d %X")
    except Exception:
        struct_time = time.strptime(format_time, "%Y-%m-%d %X")
    except:
        raise Exception("the string time has a error format, function strtotime just support 'YYYY-MM-DD hh:mm:ss' or 'YYYY/MM/DD hh:mm:ss'")

    return int(time.mktime(struct_time))


def shift(time_type: str, timestamp: int=None):
    """
    获取指定时间的偏移量之后的时间戳,偏移量单位可以为days、weeks、months、years。例如：1 days、-3 days、5 months etc.
    默认当前时间
    返回时间戳
    :param string time_type:
    :param int timestamp:
    :return int timestamp:
    """
    if timestamp is None:
        timestamp = int(time.time())

    if 'days' in time_type:
        split_arr = str(time_type).split('days')
        format_time = datetime.datetime.fromtimestamp(timestamp) + datetime.timedelta(days=int(split_arr[0]))
        return_time_stamp = time.mktime(format_time.timetuple())
    elif 'weeks' in time_type:
        split_arr = str(time_type).split('weeks')
        format_time = datetime.datetime.fromtimestamp(timestamp) + datetime.timedelta(weeks=int(split_arr[0]))
        return_time_stamp = time.mktime(format_time.timetuple())
    elif 'months' in time_type:
        split_arr = str(time_type).split('months')
        arrow_time = arrow.get(timestamp).shift(months=int(split_arr[0]))
        return_time_stamp = arrow_time.timestamp
    elif 'years' in time_type:
        split_arr = str(time_type).split('years')
        arrow_time = arrow.get(timestamp).shift(years=int(split_arr[0]))
        return_time_stamp = arrow_time.timestamp
    else:
        raise Exception('params error')

    return int(return_time_stamp)


# 时间sleep给定的几秒钟
def sleep(second: int):
    time.sleep(int(second))


