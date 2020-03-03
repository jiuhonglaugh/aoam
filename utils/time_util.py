#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time


def getTime(format='%Y-%m-%d %H:%M:%S'):
    return time.strftime(format, time.localtime(time.time()))


def sleep(mm):
    time.sleep(mm)

if __name__ == '__main__':
    print(getTime(format='%Y-%m-%d'))