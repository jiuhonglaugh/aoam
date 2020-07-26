#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import sys

sys.path.append('/zywa/aoam')
import re

from utils.logger import logger
from utils import config_util, exeCmd
from utils.environment_util import environment_util

env = environment_util()
conf = config_util.getDict('kafka')
log = logger(loggername='kafka')


def getKafka(hostAndPorts):
    dicts = {}
    for hostAndPort in hostAndPorts:
        host = hostAndPort.split(':')[0]
        dicts[host] = 'Kafka'
    return dicts


def startKafka(host, server):
    KAFKA_HOME = env.KAFKA_HOME
    log.warn('开始启动 {host} 节点 {server} 服务'.format(host=host, server=server))
    _shell = 'ansible client -l {host} -a "{KAFKA_HOME}'.format(host=host, KAFKA_HOME=KAFKA_HOME)
    _shell = _shell + '/{scriptName}"'.format(scriptName=conf.get('kafka.start.script'))
    exeCmd.run(_shell)


def checkServerProcess():
    hostAndPorts = conf.get('kafka.hosts')
    serverlist = getKafka(hostAndPorts.split(','))

    proNum = conf.get('kafka.process.number')
    if proNum == '':
        proNum = 1
    else:
        proNum = int(proNum)

    for host in serverlist:
        content = exeCmd.execJps(host)
        nowProNum = len(re.findall(serverlist.get(host), content))

        if nowProNum < proNum:
            log.warn('{host} 节点 {proNum} 个 Kafka 服务未运行'.format(host=host, proNum=(proNum - nowProNum)))
            startKafka(host, 'Kafka')
        else:
            log.info('{host} 节点 {proNum} 个 Kafka  服务正在运行'.format(host=host, proNum=proNum))


if __name__ == '__main__':
    if conf is None:
        sys.exit()
    checkServerProcess()
