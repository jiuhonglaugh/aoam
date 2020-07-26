#!/usr/bin/env python
# -*- coding:utf-8 -*-

import configparser
import sys
from os.path import dirname, abspath

"""
获取配置文件信息
"""
configPath = dirname(dirname(abspath(__file__))) + '/config/application.properties'

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
    try:
        list = cf.items(section)
        for tuple in list:
            dt[tuple[0]] = tuple[1]
        return dt
    except:
        print(configPath + ' 配置文件中不存在: ' + section + ' 配置项')
        return None

if __name__ == '__main__':
    conf = getDict('azkaban1')
    print(conf.get("azkaban.web.hosts"))
