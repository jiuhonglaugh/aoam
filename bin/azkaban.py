#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import sys
sys.path.append('/zywa/aoam')
import re

from utils.logger import logger
from utils import config_util, exeCmd
from utils.environment_util import environment_util

env = environment_util()
conf = config_util.getDict('azkaban')
log = logger(loggername='azkaban')


def getWeb(hostAndPorts):
    dicts = {}
    for hostAndPort in hostAndPorts:
        host = hostAndPort.split(':')[0]
        dicts[host] = 'AzkabanWebServer'
    return dicts


def getExe(keys, dicts):
    for key in keys:
        key = key.split(':')[0]
        if key in dicts:
            dicts[key] = dicts[key] + ',AzkabanExecutorServer'
        else:
            dicts[key] = 'AzkabanExecutorServer'
    return dicts


def startAzkaban(host, server):
    AZKABAN_HOME = env.AZKABAN_HOME
    log.warn('开始启动 {host} 节点 {server} 服务'.format(host=host, server=server))
    _shell = 'ssh {host} -a {AZKABAN_HOME}'.format(host=host, AZKABAN_HOME=AZKABAN_HOME)
    if "AzkabanWebServer".find(server) >= 0:
        _shell = _shell + '/azkaban-web-server/start-web.sh'
        exeCmd.run(_shell)
    else:
        _shell = _shell + '/azkaban-exec-server/start-exec.sh'
        exeCmd.run(_shell)


def checkServerProcess():
    webHostAndPorts = conf.get('azkaban.web.hosts')
    serverProcessList = getWeb(webHostAndPorts.split(','))
    execHostAndPorts = conf.get('azkaban.exe.hosts')
    serverProcessList = getExe(execHostAndPorts.split(','), serverProcessList)
    for host in serverProcessList:
        content = exeCmd.execJps(host)
        for serverName in serverProcessList.get(host).split(','):
            if len(re.findall(serverName, content)) < 1:
                log.warn('{host} 节点 {serverName} 服务未运行'.format(host=host, serverName=serverName))
                startAzkaban(host, serverName)
            else:
                log.info('{host} 节点 {serverName} 服务正在运行'.format(host=host, serverName=serverName))


if __name__ == '__main__':
    checkServerProcess()
