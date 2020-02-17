#!/usr/bin/env python
# -*- coding:utf-8 -*-

import configparser
import os

"""
获取配置文件信息
"""

root_dir = os.path.dirname(os.path.abspath('.'))
configPath = os.path.join(root_dir, "config/logger.conf")
###必须使用RawConfigParser()，否则会报错
cf = configparser.RawConfigParser()
# 读取配置文件，如果写文件的绝对路径，就可以不用os模块
cf.read(configPath)

"""
获取所有顶级配置
"""


def getAllSections():
    sections = cf.sections()
    return sections


"""
获取全部
"""


def getDicts():
    dt = {}
    for sect in getAllSections():
        list = cf.items(sect)
        for tuple in list:
            dt[tuple[0]] = tuple[1]
    return dt


"""
获取单个
"""


def getDict(section):
    dt = {}
    list = cf.items(section)
    for tuple in list:
        dt[tuple[0]] = tuple[1]
    return dt


if __name__ == '__main__':
    conf = getDicts(getAllSections())
    print(conf.get("password"))
