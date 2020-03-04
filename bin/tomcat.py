#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import sys

sys.path.append('/zywa/aoam')
import re

from utils.logger import logger
from utils import config_util, exeCmd
from utils.environment_util import environment_util

env = environment_util()
conf = config_util.getDict('tomcat')
log = logger(loggername='tomcat')


def getBootstrap(hostAndPorts):
    dicts = {}
    proNumDicts = {}
    proNums = conf.get('tomcat.process.number').split(',')
    i = 0
    for hostAndPort in hostAndPorts:
        host = hostAndPort.split(':')[0]
        dicts[host] = 'Bootstrap'
        proNumDicts[host] = proNums[i]
        i += 1
    return dicts, proNumDicts


def startBootstrap(host, server):
    log.warn('开始启动 {host} 节点 {server} 服务'.format(host=host, server=server))
    _shell = 'ansible client -l {host} -a "'.format(host=host)
    _shell = _shell + '{startScriptPath}"'.format(startScriptPath=conf.get('tomcat.start.script.path'))
    exeCmd.run(_shell)


def checkServerProcess():
    hostAndPorts = conf.get('tomcat.hosts')
    serverlist, proNums = getBootstrap(hostAndPorts.split(','))
    for host in serverlist:
        content = exeCmd.execJps(host)
        nowProNum = len(re.findall(serverlist.get(host), content))
        proNum = int(proNums.get(host))
        if nowProNum < proNum:
            log.warn('{host} 节点 {proNum} 个 Bootstrap  服务未运行'.format(host=host, proNum=(proNum - nowProNum)))
            startBootstrap(host, 'Bootstrap')
        else:
            log.info('{host} 节点 {proNum} 个 Bootstrap  服务正在运行'.format(host=host, proNum=proNum))


if __name__ == '__main__':
    checkServerProcess()
