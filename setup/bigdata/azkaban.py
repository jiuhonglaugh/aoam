#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import sys

sys.path.append('/zywa/aoam')
import re
import os
from setup.utils.logger import logger
from setup.utils import config_util
from setup.utils import exeCmd

conf = config_util.getDict('azkaban')
log = logger(loggername='azkaban')


def getWeb(hostAndPorts):
    dict = {}
    for hostAndPort in hostAndPorts:
        host = hostAndPort.split(':')[0]
        dict[host] = 'AzkabanWebServer'
    return dict


def getExe(keys, dict):
    for key in keys:
        key = key.split(':')[0]
        if key in dict:
            dict[key] = dict[key] + ',AzkabanExecutorServer'
        else:
            dict[key] = 'AzkabanExecutorServer'
    return dict


def startAzkaban(host, server):
    AZKABAN_HOME = os.getenv('AZKABAN_HOME')
    # AZKABAN_EXE_HOME = os.getenv('AZKABAN_HOME')
    log.warn('开始启动 {host} 节点的 {server} 服务\n'.format(host=host, server=server))
    _shell = 'ansible client -l {host} -a "{AZKABAN_HOME}'.format(host=host, AZKABAN_HOME=AZKABAN_HOME)
    if "AzkabanWebServer".find(server) >= 0:
        _shell = _shell + '/azkaban-web-server/start-web.sh"'
        exeCmd.run(_shell)
    else:
        _shell = _shell + '/azkaban-exec-server/start-exec.sh"'
        exeCmd.run(_shell)


def checkServerProcess():
    hostAndPorts = conf.get('azkaban.web.hosts')
    serverlist = getWeb(hostAndPorts.split(','))
    hostAndPorts = conf.get('azkaban.exe.hosts')
    serverlist = getExe(hostAndPorts.split(','), serverlist)
    for host in serverlist:
        content = exeCmd.Popen('ansible client -l {host} -a "jps"'.format(host=host))
        for server in serverlist.get(host).split(','):
            if (len(re.findall(server, content)) < 1):
                log.warn('{host} 节点的 {server} 服务未运行'.format(host=host, server=server))
                startAzkaban(host, server)
            else:
                log.info('{host} 节点  {server} 服务正在运行\n'.format(host=host, server=server))


if __name__ == '__main__':
    checkServerProcess()
