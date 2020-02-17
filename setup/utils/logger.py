#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
from setup.utils import config_util

conf = config_util.getDict('LOG-CONF')


class logger:
    def __init__(self, clevel=logging.INFO, Flevel=logging.WARN):
        self.logger = logging.getLogger(conf.get('logs-path'))
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter(conf.get('logs-format'))
        # 设置Console日志
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(clevel)
        # 设置文件日志
        fh = logging.FileHandler(filename=conf.get('logs-path'), encoding='utf-8')
        fh.setFormatter(fmt)
        fh.setLevel(Flevel)
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
if __name__ == '__main__':
    logger.info("asd")