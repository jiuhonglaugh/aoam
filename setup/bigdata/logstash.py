#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from setup.utils.logger import logger
from setup.utils import config_util
from setup.utils import exeCmd
import re
import os
from elasticsearch import Elasticsearch

conf = config_util.getDict('storm')
log = logger(loggername='storm')

'''
检测索引是否存在，如果集群挂了，是无法返回索引的存在与否


def checkServer():
    hostAndPorts = conf.get('hosts')
    es = Elasticsearch(hostAndPorts)
    #print(es.indices.exists(index="test"))  #填写对应索引
    lists = es.cluster.health()
    logger.info("elasticsearch集群状态：",end="")
    ES_cluster_status = lists["status"]
    if ES_cluster_status == "green":
        logger.info("####集群处于健康状态####")
    elif ES_cluster_status == "yellow":
        logger.info("集群处于亚健康状态")
    elif ES_cluster_status == "red":
        logger.warn("集群挂了")
    logger.info("elasticsearch集群节点数："+lists['number_of_nodes'])
    logger.info("elasticsearch集群节点数："+lists['number_of_data_nodes'])
'''
#某个host主机上有nimbus和core
def getNimbus(hostAndPorts):
    _list = []
    dict_nimbus = {}
    dict_core = {}
    for hostAndPort in hostAndPorts:
        host = hostAndPort.split(':')[0]
        dict_nimbus[host] = 'nimbus'
        dict_core[host] = 'core'
    _list.append = dict_nimbus
    _list.append = dict_core
    return _list

'''
 某个host主机上有supervisor
 返回一个字典：{'XXXX':'supervisor','XXXXX':'supervisor'}
'''
def getSupervisor(hostAndPorts):
    dict = {}
    for hostAndPort in hostAndPorts:
        host = hostAndPort.split(':')[0]
        dict[host] = 'Supervisor'
    return dict

def startStorm(host, server):
    STORM_HOME = os.getenv('STORM_HOME')
    log.warn('开始启动 ' + host + ' 节点的 ' + server + ' 服务\n')
    _shell = 'ansible client -l ' + host + ' -a "' + STORM_HOME + '/start.sh"'
    exeCmd.run(_shell)


def checkServerProcess():
    masterHostAndPorts = conf.get('storm.hosts.nimbus')
    supervisorHostAndPorts = conf.get('storm.hosts.supervisor')
    masterServerList = getStorm(nimbusHostAndPorts.split(','))
    nimbusServerList = masterServerList[0]
    coreServerList = masterServerList[1]
    supervisorServerList = getSupervisor(supervisorHostAndPorts.split(','))
    for host in coreServerList:
        content = exeCmd.Popen('ansible client -l ' + host + ' -a "jps"')
        if (len(re.findall(coreServerList.get(host), content)) < 1):
            log.warn(host + ' 节点的 ' + 'Storm---UI' + ' 服务未运行')
            startStorm(host, 'Storm')
        else:
            log.info(host + ' 节点的 ' + ' Storm---nimbus ' + '服务正在运行')
    for host in nimbusServerList:
        content = exeCmd.Popen('ansible client -l ' + host + ' -a "jps"')
        if (len(re.findall(nimbusServerList.get(host), content)) < 1):
            log.warn(host + ' 节点的 ' + 'Storm---nimbus' + ' 服务未运行')
            startStorm(host, 'Storm')
        else:
            log.info(host + ' 节点的 ' + ' Storm---nimbus ' + '服务正在运行')
    for host in supervisorServerList:
        content = exeCmd.Popen('ansible client -l ' + host + ' -a "jps"')
        if (len(re.findall(supervisorServerList.get(host), content)) < 1):
            log.warn(host + ' 节点的 ' + 'Storm---supervisor' + ' 服务未运行')
            startStorm(host, 'Storm')
        else:
            log.info(host + ' 节点的 ' + 'Storm---supervisor' + '服务正在运行')

if __name__ == '__main__':
    checkServerProcess()
    #checkServer()
