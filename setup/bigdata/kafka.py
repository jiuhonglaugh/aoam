#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import sys

sys.path.append('/zywa/aoam')
import re
import os
from setup.utils.logger import logger
from setup.utils import config_util
from setup.utils import exeCmd

conf = config_util.getDict('zookeeper')
log = logger(loggername='zookeeper')


def getQuorumPeerMain(hostAndPorts):
    dict = {}
    for hostAndPort in hostAndPorts:
        host = hostAndPort.split(':')[0]
        dict[host] = 'QuorumPeerMain'
    return dict


def startZk(host, server):
    ZOOKEEPER_HOME = os.getenv('ZOOKEEPER_HOME')
    log.warn('开始启动 {host} 节点的 {server} 服务\n'.format(host=host, server=server))
    _shell = 'ansible client -l {host} -a "{ZOOKEEPER_HOME}'.format(host=host, ZOOKEEPER_HOME=ZOOKEEPER_HOME)
    _shell = _shell + '/bin/zkServer.sh start"'
    exeCmd.run(_shell)


def checkServerProcess():
    hostAndPorts = conf.get('hosts')
    serverlist = getQuorumPeerMain(hostAndPorts.split(','))
    for host in serverlist:
        content = exeCmd.Popen('ansible client -l {host} -a "jps"'.format(host=host))
        if (len(re.findall(serverlist.get(host), content)) < 1):
            log.warn('{host} 节点的  QuorumPeerMain  服务未运行'.format(host=host))
            startZk(host, 'QuorumPeerMain')
        else:
            log.info('{host} 节点的   QuorumPeerMain  服务正在运行'.format(host=host))


if __name__ == '__main__':
    checkServerProcess()
