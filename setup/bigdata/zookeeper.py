#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from setup.utils.logger import logger
from setup.utils import config_util
from setup.utils import exeCmd
import sys
sys.path.append('/zywa/aoam')
import re
import os

conf = config_util.getDict('zookeeper')
log = logger()


def getQuorumPeerMain(hostAndPorts):
    dict = {}
    for hostAndPort in hostAndPorts:
        host = hostAndPort.split(':')[0]
        dict[host] = 'QuorumPeerMain'
    return dict


def startZk(host, server):
    ZOOKEEPER_HOME = os.getenv('ZOOKEEPER_HOME')
    log.warn('开始启动 ' + host + ' 节点的 ' + server + ' 服务\n')
    _shell = 'ansible client -l ' + host + ' -a "' + ZOOKEEPER_HOME + '/bin/zkServer.sh start"'
    exeCmd.run(_shell)



def checkServerProcess():
    hostAndPorts = conf.get('hosts')
    serverlist = getQuorumPeerMain(hostAndPorts.split(','))
    for host in serverlist:
        content = exeCmd.Popen('ansible client -l ' + host + ' -a "jps"')
        if (len(re.findall(serverlist.get(host), content)) < 1):
            log.warn(host + ' 节点的 ' + 'QuorumPeerMain' + ' 服务未运行')
            startZk(host, 'QuorumPeerMain')
        else:
            log.info(host + ' 节点的 ' + ' QuorumPeerMain ' + '服务正在运行')


if __name__ == '__main__':
    checkServerProcess()
