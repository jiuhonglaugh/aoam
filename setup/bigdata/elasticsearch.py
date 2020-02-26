#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sys
sys.path.append('/zywa/aoam')
from setup.utils.logger import logger
from setup.utils import config_util
from setup.utils import exeCmd
import re
import os
#from elasticsearch import Elasticsearch

conf = config_util.getDict('elasticsearch')
log = logger(loggername='elasticsearch')

'''
判断传入的ip等参数是否存在端口
1）存在端口
2）不存在端口
'''
def checkExistPort(hostsOrhosts_Port):
    hosts = hostsOrhosts_Port[0]
    if hosts.find(':') != -1:
        return True
    else:
        return False


'''
检测索引是否存在，如果集群挂了，是无法返回索引的存在与否
'''

'''
def checkServer():
    hostAndPorts = conf.get('hosts')
    es = Elasticsearch(hostAndPorts)
    # print(es.indices.exists(index="test"))  #填写对应索引
    lists = es.cluster.health()
    logger.info("elasticsearch集群状态：")
    ES_cluster_status = lists["status"]
    if ES_cluster_status == "green":
        logger.info("####集群处于健康状态####")
    elif ES_cluster_status == "yellow":
        logger.info("集群处于亚健康状态")
    elif ES_cluster_status == "red":
        logger.warn("集群挂了")
    logger.info("elasticsearch集群节点数：" + lists['number_of_nodes'])
    logger.info("elasticsearch集群节点数：" + lists['number_of_data_nodes'])
'''

def getES(hostAndPorts):
    dict = {}
    isExist = checkExistPort(hostAndPorts)
    for hostAndPort in hostAndPorts:
        if isExist == True:
            host = hostAndPort.split(':')[0]   #有IP的，有端口
            dict[host] = 'Elasticsearch'
        else:
            dict[hostAndPort] = 'Elasticsearch'  #如果只有IP的，无端口
    return dict

'''
def startES(host, server):
    ELASTICSEARCH_HOME = os.getenv('ELASTICSEARCH_HOME')
    log.warn('开始启动 ' + host + ' 节点的 ' + server + ' 服务')
    _shell = 'ansible client -l ' + host + ' -a "' + ELASTICSEARCH_HOME + '/start.sh"'
    exeCmd.run(_shell)
'''
def startES(host, server):
    ELASTICSEARCH_HOME = os.getenv('ELASTICSEARCH_HOME')
    _shell = 'ansible client -l ' + host + ' -a "'
    log.warn('开始启动 ' + host + ' 节点的 ' + server + ' 服务')
    _shell = _shell +  '{ELASTICSEARCH_HOME}/start.sh"'.format(ELASTICSEARCH_HOME=ELASTICSEARCH_HOME)
    exeCmd.run(_shell)

def checkServerProcess():
    hostAndPorts = conf.get('es.hosts')
    print(hostAndPorts)
    serverlist = getES(hostAndPorts.split(','))
    for host in serverlist:
        content = exeCmd.execJps(host)
        if (len(re.findall(serverlist.get(host), content)) < 1):
            log.warn(host + ' 节点的 ' + 'Elasticsearch' + ' 服务未运行')
            startES(host, 'Elasticsearch')
        else:
            log.info(host + ' 节点的 ' + ' Elasticsearch ' + '服务正在运行')


if __name__ == '__main__':
    checkServerProcess()
    #checkServer()
