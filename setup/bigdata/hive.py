#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import sys

sys.path.append('/zywa/aoam')
import re
import os
from setup.utils.logger import logger
from setup.utils import config_util
from setup.utils import exeCmd

conf = config_util.getDict('hive')
log = logger(loggername='hive')


def getHiveServer2(hostAndPorts):
    dict = {}
    for hostAndPort in hostAndPorts:
        host = hostAndPort.split(':')[0]
        dict[host] = 'org.apache.hive.service.server.HiveServer2'
    return dict


def getHiveMetaStore(keys, dict):
    for key in keys:
        key = key.split(':')[0]
        if key in dict:
            dict[key] = dict[key] + ',org.apache.hadoop.hive.metastore.HiveMetaStore'
        else:
            dict[key] = 'org.apache.hadoop.hive.metastore.HiveMetaStore'
    return dict


def startHive(host, server):
    HIVE_HOME = os.getenv('HIVE_HOME')
    log.warn('开始启动 ' + host + ' 节点的 ' + server + ' 服务\n')
    _shell = 'ansible client -l {host} -a "{HIVE_HOME}/bin/hive --service '.format(host=host, HIVE_HOME=HIVE_HOME)
    if "org.apache.hadoop.hive.metastore.HiveMetaStore".find(server):
        _shell = _shell + 'metastore > {HIVE_HOME}/metastore.log 2>&1 &"'.format(HIVE_HOME=HIVE_HOME)
        exeCmd.run(_shell)
    else:
        _shell = _shell + 'hiveserver2 > {HIVE_HOME}/hiveserver2.log 2>&1 &"'.format(HIVE_HOME=HIVE_HOME)
        exeCmd.run(_shell)


def checkServerProcess():
    hostAndPorts = conf.get('hive.server2')
    serverlist = getHiveServer2(hostAndPorts.split(','))
    hostAndPorts = conf.get('hive.metastore')
    serverlist = getHiveMetaStore(hostAndPorts.split(','), serverlist)
    for host in serverlist:
        content = exeCmd.Popen('ansible client -l {host} -a "jps -m"'.format(host=host))
        for server in serverlist.get(host).split(','):
            if (len(re.findall(server, content)) < 1):
                log.warn('{host} 节点的 {server} 服务未运行'.format(host=host, server=server))
                startHive(host, server)
            else:
                log.info('{host} 节点  {server} 服务正在运行\n'.format(host=host, server=server))


if __name__ == '__main__':
    checkServerProcess()
