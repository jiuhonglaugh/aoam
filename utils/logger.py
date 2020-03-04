#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging

from utils import config_util
from utils import time_util
from utils import file_util

conf = config_util.getDict('log-conf')

'''
loggername 参数最好指定，如果不指定可能会导致日志重复输出
'''


class logger:
    def __init__(self, loggername='default'):
        self.logger = logging.getLogger(loggername)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter(conf.get('logs.format'))
        # 设置Console日志
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(getLevel(conf.get('logs.clevel')))
        # 设置文件日志
        logsPath = file_util.getHome() + '/logs/aoam.log'

        fh = logging.FileHandler(filename=sP(logsPath), encoding='utf-8')
        fh.setFormatter(fmt)
        fh.setLevel(getLevel(conf.get('logs.flevel')))
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def cri(self, message):
        self.logger.critical(message)


def getLevel(level):
    if level.lower() == 'error':
        return logging.ERROR
    elif level.lower() == 'warn':
        return logging.WARN
    elif level.lower() == 'debug':
        return logging.DEBUG
    else:
        return logging.INFO


def sP(oldPath, symbol='/'):
    args = oldPath.split(symbol)
    fileName = args[-1]
    fileLen = len(args[-1])
    filepath = oldPath[:-fileLen] + time_util.getTime('%Y-%m-%d') + '-' + fileName
    return filepath


if __name__ == '__main__':
    # log = logger()
    # log.info("asd")

    print(sP('../logs/aoam.log', '/'))
    #
    # for str in strs.split('/'):
    #     print(str)
