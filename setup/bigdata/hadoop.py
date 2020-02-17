#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from hdfs import InsecureClient
import configparser
from setup.utils.logger import logger
from setup.utils import time_util
from setup.utils import file_util

log = logger()
config = configparser.ConfigParser()
config.read('../config/bigdata.conf')
client = InsecureClient(config['hadoop']['name.node.ui'], user=config['hadoop']['name.node.user'], root='/')

'''
创建hdfs文件夹
'''


def _mkdir(path):
    client.makedirs(path)


def _createFile(path, fileName, data):
    _mkdir(path)
    filePath = file_util.repairPath(path) + fileName
    log.info('开始删除hdfs上的' + filePath + '文件')
    if _delete(filePath):
        with client.write(filePath, append=False) as w:
            log.info('开始向hdfs测试写入' + filePath + '文件')
            w.write(bytes(data, encoding='utf-8'))
            log.info('向hdfs写入' + filePath + '文件成功')


def _delete(filePath):
    flag = True
    try:
        client.delete(filePath)
    except:
        flag = False
        log.error("删除hdfs " + filePath + "文件失败")
    return flag


def checkService():
    nowTime = time_util.getTime()
    data = nowTime + ':  此文件是自动化运维软件测试使用，用来判断hadoop集群是否正常工作的一项指标，请勿删除\n'
    hdfspath = config['hadoop']['name.node.path']
    fileName = config['hadoop']['name.node.file.name']
    _createFile(hdfspath, fileName, data)


if __name__ == '__main__':
    checkService()
