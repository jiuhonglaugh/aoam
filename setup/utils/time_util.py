#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time


def getTime(format='%Y-%m-%d %H:%M:%S'):
    return time.strftime(format, time.localtime(time.time()))
