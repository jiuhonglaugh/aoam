#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import sys

sys.path.append('/zywa/aoam')
import re
from setup.utils.logger import logger
from setup.utils import config_util
from setup.utils import exeCmd
from setup.utils.environment_util import environment_util

env = environment_util()
conf = config_util.getDict('zookeeper')
log = logger(loggername='zookeeper')


def getQuorumPeerMain(hostAndPorts):
    dicts = {}
    for hostAndPort in hostAndPorts:
        host = hostAndPort.split(':')[0]
        dicts[host] = 'QuorumPeerMain'
    return dicts


def startZk(host, server):
    ZOOKEEPER_HOME = env.ZOOKEEPER_HOME
    log.warn('开始启动 {host} 节点的 {server} 服务\n'.format(host=host, server=server))
    _shell = 'ansible client -l {host} -a "{ZOOKEEPER_HOME}'.format(host=host, ZOOKEEPER_HOME=ZOOKEEPER_HOME)
    _shell = _shell + '/bin/zkServer.sh start"'
    exeCmd.run(_shell)


def checkServerProcess():
    hostAndPorts = conf.get('zookeeper.hosts')
    serverlist = getQuorumPeerMain(hostAndPorts.split(','))
    for host in serverlist:
        content = exeCmd.execJps(host)
        if len(re.findall(serverlist.get(host), content)) < 1:
            log.warn('{host} 节点的  QuorumPeerMain  服务未运行'.format(host=host))
            startZk(host, 'QuorumPeerMain')
        else:
            log.info('{host} 节点的   QuorumPeerMain  服务正在运行'.format(host=host))


if __name__ == '__main__':
    checkServerProcess()
