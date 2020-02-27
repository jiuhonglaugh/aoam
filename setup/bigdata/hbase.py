#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
sys.path.append('/zywa/aoam')
import re

from setup.utils.logger import logger
from setup.utils import file_util
from setup.utils import xml_util
from setup.utils import exeCmd
from setup.utils.environment_util import environment_util

env = environment_util()
log = logger(loggername='hbase')


def getHbaseXml(configPath):
    hbaseXml = {}
    tmp = xml_util.getXml(configPath + 'hbase-site.xml', 'property')
    hbaseXml['hbase.master'] = tmp.get('hbase.master')
    hbaseXml['hbase.zookeeper.quorum'] = tmp.get('hbase.zookeeper.quorum')
    hbaseXml['hbase.zookeeper.property.clientPort'] = tmp.get('hbase.zookeeper.property.clientPort')
    hbaseXml['hbase.master.info.port'] = tmp.get('hbase.master.info.port')

    return hbaseXml


def getHRegionServer(path):
    dicts = {}
    with open(file_util.repairPath(path) + 'regionservers') as r:
        for line in r.readlines():
            dicts[line.strip()] = 'HRegionServer'
    return dicts


def getHMaster(keys, dicts):
    key = keys.get('hbase.master')
    if key in dicts:
        dicts[key] = dicts[key] + ',HMaster'
    else:
        dicts[key] = 'HMaster'
    return dicts


def checkServerProcess():
    dictXml = getHbaseXml(file_util.repairPath('../config/'))
    serverProcess = getHRegionServer('../config/')
    return getHMaster(dictXml, serverProcess)


def exeCheckServerProcess():
    serverList = checkServerProcess()
    for host in serverList:
        content = exeCmd.execJps(host)
        for serverName in serverList.get(host).split(','):
            if len(re.findall(serverName, content)) < 1:
                log.warn('{host} 节点的  {serverName} 服务未运行'.format(host=host, serverName=serverName))
                startHbase(host, serverName.lower())
            else:
                log.info('{host} 节点 {serverName} 服务正在运行'.format(host=host, serverName=serverName))


def startHbase(host, serverName):
    HBASE_HOME = env.HBASE_HOME
    _shell = 'ansible client -l {host} -a "{HBASE_HOME}/bin/hbase-daemons.sh start '.format(host=host,
                                                                                            HBASE_HOME=HBASE_HOME)
    if 'hmaster'.find(serverName) >= 0:
        log.warn('开始启动  {host} 节点的 {serverName} 服务'.format(host=host, serverName=serverName))
        _shell = _shell + 'master"'
        exeCmd.run(_shell)
    else:
        log.warn('开始启动 {host} 节点的 {serverName} 服务'.format(host=host, serverName=serverName))
        _shell = _shell + 'regionserver"'
        exeCmd.run(_shell)


if __name__ == '__main__':
    exeCheckServerProcess()
