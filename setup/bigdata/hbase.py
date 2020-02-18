#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys

sys.path.append('/zywa/aoam')
import os
import re
from setup.utils.logger import logger
from setup.utils import file_util
from setup.utils import xml_util
from setup.utils import exeCmd

log = logger()


def getHadoopXml(configPath):
    hbaseXml = {}
    tmp = xml_util.getXml(configPath + 'hbase-site.xml', 'property')
    hbaseXml['hbase.master'] = tmp.get('hbase.master')
    hbaseXml['hbase.zookeeper.quorum'] = tmp.get('hbase.zookeeper.quorum')
    hbaseXml['hbase.zookeeper.property.clientPort'] = tmp.get('hbase.zookeeper.property.clientPort')
    hbaseXml['hbase.master.info.port'] = tmp.get('hbase.master.info.port')

    return hbaseXml


def getHRegionServer(path):
    dict = {}
    with open(file_util.repairPath(path) + 'regionservers') as r:
        for line in r.readlines():
            dict[line.strip()] = 'HRegionServer'
    return dict


def getHMaster(keys, dict):
    key = keys.get('hbase.master')
    if key in dict:
        dict[key] = dict[key] + ',HMaster'
    else:
        dict[key] = 'HMaster'
    return dict


def checkServerProcess():
    list = getHadoopXml(file_util.repairPath('../config/'))
    serverProcess = getHRegionServer('../config/')
    serverProcess = getHMaster(list, serverProcess)
    return serverProcess


def exeCheckServerProcess():
    serverList = checkServerProcess()
    for node in serverList:
        content = exeCmd.Popen('ansible client -l {node} -a "jps"'.format(node=node))
        for server in serverList.get(node).split(','):
            if (len(re.findall(server, content)) < 1):
                log.warn('{node} 节点的  {server} 服务未运行'.format(node=node, server=server))
                startHbase(node, server.lower())
            else:
                log.info('{node} 节点 {server} 服务正在运行\n'.format(node=node, server=server))


def startHbase(ip, name):
    HBASE_HOME = os.getenv('HBASE_HOME')
    _shell = 'ansible client -l {ip} -a "{HBASE_HOME}/bin/hbase-daemons.sh start '.format(ip=ip, HBASE_HOME=HBASE_HOME)
    if ('hmaster'.find(name) >= 0):
        log.warn('开始启动  {ip} 节点的 {name} 服务\n'.format(ip=ip, name=name))
        _shell = _shell + 'master"'
        exeCmd.run(_shell)
    else:
        log.warn('开始启动 {ip} 节点的 {name} 服务\n'.format(ip=ip, name=name))
        _shell = _shell + 'regionserver"'
        exeCmd.run(_shell)


if __name__ == '__main__':
    exeCheckServerProcess()
