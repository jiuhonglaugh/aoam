#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from hdfs import InsecureClient
import sys

sys.path.append('/zywa/aoam')
import re
from setup.utils.logger import logger
from setup.utils import time_util
from setup.utils import file_util
from setup.utils import xml_util
from setup.utils import exeCmd
from setup.utils.environment_util import environment_util

env = environment_util()
log = logger(loggername='hadoop')
hdfsXml = xml_util.getXml('../config/hdfs-site.xml', 'property')
client = InsecureClient('http://' + hdfsXml['dfs.http.address'], user='hadoop', root='/')

'''
创建hdfs文件夹
'''


def _mkdir(path):
    client.makedirs(path)


def _createFile(path, fileName, data):
    _mkdir(path)
    filePath = file_util.repairPath(path) + fileName
    log.info('开始删除hdfs上的' + filePath + '文件')
    if _delete(filePath):
        with client.write(filePath, append=False) as w:
            log.info('开始向hdfs测试写入' + filePath + '文件')
            w.write(bytes(data, encoding='utf-8'))
            log.info('向hdfs写入' + filePath + '文件成功')


def _delete(filePath):
    flag = True
    try:
        client.delete(filePath)
    except:
        flag = False
        log.error("删除hdfs " + filePath + "文件失败")
    return flag


def checkService():
    nowTime = time_util.getTime()
    data = nowTime + ':  此文件是自动化运维软件测试使用，用来判断hadoop集群是否正常工作的一项指标，请勿删除\n'
    hdfspath = '/aoam/'
    fileName = 'aoam.txt'
    _createFile(hdfspath, fileName, data)


def getHadoopXml(configPath):
    hadoopXml = {}
    tmp = xml_util.getXml(configPath + 'hdfs-site.xml', 'property')
    hadoopXml['dfs.http.address'] = tmp.get('dfs.http.address')
    hadoopXml['dfs.namenode.secondary.http-address'] = tmp.get('dfs.namenode.secondary.http-address')

    tmp = xml_util.getXml(configPath + 'core-site.xml', 'property')
    hadoopXml['fs.defaultFS'] = tmp.get('fs.defaultFS')

    tmp = xml_util.getXml(configPath + 'yarn-site.xml', 'property')
    hadoopXml['yarn.resourcemanager.webapp.address'] = tmp.get('yarn.resourcemanager.webapp.address')
    hadoopXml['yarn.resourcemanager.hostname'] = tmp.get('yarn.resourcemanager.hostname')
    hadoopXml['yarn.log.server.web-service.url'] = tmp.get('yarn.log.server.web-service.url')
    hadoopXml['yarn.log.server.url'] = tmp.get('yarn.log.server.url')

    tmp = xml_util.getXml(configPath + 'mapred-site.xml', 'property')
    hadoopXml['mapreduce.jobhistory.address'] = tmp.get('mapreduce.jobhistory.address')
    hadoopXml['mapreduce.jobhistory.webapp.address'] = tmp.get('mapreduce.jobhistory.webapp.address')

    return hadoopXml


def getDataNodeAndNodeManager(path):
    dict = {}
    with open(file_util.repairPath(path) + 'slaves') as r:
        for line in r.readlines():
            dict[line.strip()] = 'DataNode,NodeManager'
    return dict


def getNameNode(keys, dict):
    key = keys.get('dfs.http.address').split(':')[0]
    if key in dict:
        dict[key] = dict[key] + ',NameNode'
    else:
        dict[key] = 'NameNode'
    return dict


def getSecondNameNode(keys, dict):
    key = keys.get('dfs.namenode.secondary.http-address').split(':')[0]
    if key in dict:
        dict[key] = dict[key] + ',SecondaryNameNode'
    else:
        dict[key] = 'SecondaryNameNode'
    return dict


def getResourceManager(keys, dict):
    key = keys.get('yarn.resourcemanager.hostname')
    if key in dict:
        dict[key] = dict[key] + ',ResourceManager'
    else:
        dict[key] = 'ResourceManager'
    return dict


def getHistoryServer(keys, dict):
    key = keys.get('yarn.log.server.url').split(":")[1].replace('//', '')
    if key in dict:
        dict[key] = dict[key] + ',JobHistoryServer'
    else:
        dict[key] = 'JobHistoryServer'
    return dict


def checkServerProcess():
    list = getHadoopXml(file_util.repairPath('../config/'))
    serverProcess = getDataNodeAndNodeManager('../config/')
    serverProcess = getNameNode(list, serverProcess)
    serverProcess = getSecondNameNode(list, serverProcess)
    serverProcess = getResourceManager(list, serverProcess)
    serverProcess = getHistoryServer(list, serverProcess)
    return serverProcess


def exeCheckServerProcess():
    serverList = checkServerProcess()
    for node in serverList:
        content = exeCmd.Popen('ansible client -l {node} -a "jps"'.format(node=node))
        for server in serverList.get(node).split(','):
            if (len(re.findall(server, content)) < 1):
                log.warn('{node} 节点的 {server} 服务未运行'.format(node=node, server=server))
                start_hadoop(node, server.lower())
            else:
                log.info('{node} 节点 {server} 服务正在运行\n'.format(node=node, server=server))
    time_util.sleep(30)
    log.info('开始测试hadoop服务是否可用')
    checkService()


def start_hadoop(ip, serverName):
    HADOOP_HOME = env.HADOOP_HOME

    _shell = 'ansible client -l {ip} -a "{HADOOP_HOME}/sbin/'.format(ip=ip, HADOOP_HOME=HADOOP_HOME)

    if ('secondarynamenodenamenodedatanode'.find(serverName) >= 0):
        log.warn('开始启动 {ip} 节点的 {serverName} 服务\n'.format(ip=ip, serverName=serverName))
        _shell = _shell + 'hadoop-daemon.sh start {serverName}"'.format(serverName=serverName)
        exeCmd.run(_shell)
    elif ('resourcemanagernodemanager'.find(serverName) >= 0):
        log.warn('开始启动 {ip} 节点的 {serverName} 服务\n'.format(ip=ip, serverName=serverName))
        _shell = _shell + 'yarn-daemon.sh start {serverName}"'.format(serverName=serverName)
        exeCmd.run(_shell)
    else:
        log.warn('开始启动 {ip} 节点的 {serverName} 服务\n'.format(ip=ip, serverName=serverName))
        _shell = _shell + 'mr-jobhistory-daemon.sh start historyserver"'
        exeCmd.run(_shell)


if __name__ == '__main__':
    exeCheckServerProcess()
