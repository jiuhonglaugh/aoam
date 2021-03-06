#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import sys
sys.path.append('/zywa/aoam')
import re

from utils.logger import logger
from utils import config_util, exeCmd
from utils.environment_util import environment_util

env = environment_util()
conf = config_util.getDict('hive')
log = logger(loggername='hive')


def getHiveServer2(hostAndPorts):
    dicts = {}
    for hostAndPort in hostAndPorts:
        host = hostAndPort.split(':')[0]
        dicts[host] = 'org.apache.hive.service.server.HiveServer2'
    return dicts


def getHiveMetaStore(keys, dicts):
    for key in keys:
        key = key.split(':')[0]
        if key in dicts:
            dicts[key] = dicts[key] + ',org.apache.hadoop.hive.metastore.HiveMetaStore'
        else:
            dicts[key] = 'org.apache.hadoop.hive.metastore.HiveMetaStore'
    return dicts


def startHive(host, server):
    HIVE_HOME = env.HIVE_HOME
    log.warn('开始启动 ' + host + ' 节点 ' + server + ' 服务')
    _shell = 'ansible client -l {host} -a "{HIVE_HOME}/'.format(host=host, HIVE_HOME=HIVE_HOME)
    if "org.apache.hadoop.hive.metastore.HiveMetaStore".find(server) >= 0:
        _shell = _shell + '{scriptName}"'.format(scriptName=conf.get('hive.metastore.start.script'))
        exeCmd.run(_shell)
    else:
        _shell = _shell + '{scriptName}"'.format(scriptName=conf.get('hive.server2.start.script'))
        exeCmd.run(_shell)


def checkServerProcess():
    hostAndPorts = conf.get('hive.server2')
    serverlist = getHiveServer2(hostAndPorts.split(','))
    hostAndPorts = conf.get('hive.metastore')
    serverlist = getHiveMetaStore(hostAndPorts.split(','), serverlist)
    for host in serverlist:
        content = exeCmd.execJps(host, 'ansible client -l {host} -a "jps -m"')
        for server in serverlist.get(host).split(','):
            if len(re.findall(server, content)) < 1:
                log.warn('{host} 节点 {server} 服务未运行'.format(host=host, server=server))
                startHive(host, server)
            else:
                log.info('{host} 节点 {server} 服务正在运行'.format(host=host, server=server))


if __name__ == '__main__':
    if conf is None:
        sys.exit()
    checkServerProcess()
