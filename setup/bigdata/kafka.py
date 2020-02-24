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
conf = config_util.getDict('kafka')
log = logger(loggername='kafka')


def getKafka(hostAndPorts):
    dict = {}
    for hostAndPort in hostAndPorts:
        host = hostAndPort.split(':')[0]
        dict[host] = 'Kafka'
    return dict


def startKafka(host, server):
    KAFKA_HOME = env.KAFKA_HOME
    log.warn('开始启动 {host} 节点的 {server} 服务\n'.format(host=host, server=server))
    _shell = 'ansible client -l {host} -a "{KAFKA_HOME}'.format(host=host, KAFKA_HOME=KAFKA_HOME)
    _shell = _shell + '/{scriptName}"'.format(scriptName=conf.get('kafka.start.script'))
    exeCmd.run(_shell)


def checkServerProcess():
    hostAndPorts = conf.get('kafka.hosts')
    serverlist = getKafka(hostAndPorts.split(','))
    for host in serverlist:
        content = exeCmd.execJps(host)
        if (len(re.findall(serverlist.get(host), content)) < 1):
            log.warn('{host} 节点的  Kafka  服务未运行'.format(host=host))
            startKafka(host, 'Kafka')
        else:
            log.info('{host} 节点的   Kafka  服务正在运行'.format(host=host))


if __name__ == '__main__':
    checkServerProcess()
