#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# from hdfs import InsecureClient
import sys

sys.path.append('/zywa/aoam')
import re

from utils.logger import logger
from utils import file_util, xml_util, time_util, exeCmd
from utils.environment_util import environment_util

env = environment_util()
log = logger(loggername='hadoop')

'''
hdfsXml = xml_util.getXml('hdfs-site.xml', 'property')
client = InsecureClient('http://' + hdfsXml['dfs.http.address'], user='hadoop', root='/')

'''
# 创建hdfs文件夹
'''


def _mkdir(path):
    client.makedirs(path)


def _createFile(path, fileName, data):
    _mkdir(path)
    filePath = file_util.repairPath(path) + fileName
    log.info('开始删除hdfs上' + filePath + '文件')
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
    data = nowTime + ':  此文件是自动化运维软件测试使用，用来判断hadoop集群是否正常工作的一项指标，请勿删除'
    hdfspath = '/aoam/'
    fileName = 'aoam.txt'
    _createFile(hdfspath, fileName, data)
'''


def getHadoopXml():
    hadoopXml = {}
    tmp = xml_util.getXml('hdfs-site.xml', 'property')
    hadoopXml['dfs.http.address'] = tmp.get('dfs.http.address')
    hadoopXml['dfs.namenode.secondary.http-address'] = tmp.get('dfs.namenode.secondary.http-address')

    tmp = xml_util.getXml('core-site.xml', 'property')
    hadoopXml['fs.defaultFS'] = tmp.get('fs.defaultFS')

    tmp = xml_util.getXml('yarn-site.xml', 'property')
    hadoopXml['yarn.resourcemanager.webapp.address'] = tmp.get('yarn.resourcemanager.webapp.address')
    hadoopXml['yarn.resourcemanager.hostname'] = tmp.get('yarn.resourcemanager.hostname')
    hadoopXml['yarn.log.server.web-service.url'] = tmp.get('yarn.log.server.web-service.url')
    hadoopXml['yarn.log.server.url'] = tmp.get('yarn.log.server.url')

    tmp = xml_util.getXml('mapred-site.xml', 'property')
    hadoopXml['mapreduce.jobhistory.address'] = tmp.get('mapreduce.jobhistory.address')
    hadoopXml['mapreduce.jobhistory.webapp.address'] = tmp.get('mapreduce.jobhistory.webapp.address')

    return hadoopXml


def getDataNodeAndNodeManager():
    dicts = {}
    lines = file_util.readConfig('slaves')
    for line in lines:
        dicts[line.strip()] = 'DataNode,NodeManager'
    return dicts


def getNameNode(keys, dicts):
    key = keys.get('dfs.http.address').split(':')[0]
    if key in dicts:
        dicts[key] = dicts[key] + ',NameNode'
    else:
        dicts[key] = 'NameNode'
    return dicts


def getSecondNameNode(keys, dicts):
    key = keys.get('dfs.namenode.secondary.http-address').split(':')[0]
    if key in dicts:
        dicts[key] = dicts[key] + ',SecondaryNameNode'
    else:
        dicts[key] = 'SecondaryNameNode'
    return dicts


def getResourceManager(keys, dicts):
    key = keys.get('yarn.resourcemanager.hostname')
    if key in dicts:
        dicts[key] = dicts[key] + ',ResourceManager'
    else:
        dicts[key] = 'ResourceManager'
    return dicts


def getHistoryServer(keys, dicts):
    key = keys.get('yarn.log.server.url').split(":")[1].replace('//', '')
    if key in dicts:
        dicts[key] = dicts[key] + ',JobHistoryServer'
    else:
        dicts[key] = 'JobHistoryServer'
    return dicts


def checkServerProcess():
    dictXml = getHadoopXml()
    serverProcess = getDataNodeAndNodeManager()
    serverProcess = getNameNode(dictXml, serverProcess)
    serverProcess = getSecondNameNode(dictXml, serverProcess)
    serverProcess = getResourceManager(dictXml, serverProcess)
    return getHistoryServer(dictXml, serverProcess)


def exeCheckServerProcess():
    serverList = checkServerProcess()
    startNum = 0
    for host in serverList:
        content = exeCmd.execJps(host)
        for server in serverList.get(host).split(','):
            if len(re.findall(server, content)) < 1:
                log.warn('{host} 节点 {server} 服务未运行'.format(host=host, server=server))
                start_hadoop(host, server.lower())
                startNum += 1
            else:
                log.info('{host} 节点 {server} 服务正在运行'.format(host=host, server=server))
    if startNum > 0:
        log.warn("检测到有 {startNum} 个hadoop进程重启".format(startNum=startNum))
        time_util.sleep(30)
    # log.info('开始测试hadoop服务是否可用')
    # checkService()


def start_hadoop(host, serverName):
    HADOOP_HOME = env.HADOOP_HOME
    _shell = 'ansible client -l {host} -a "{HADOOP_HOME}/sbin/'.format(host=host, HADOOP_HOME=HADOOP_HOME)
    if 'secondarynamenodenamenodedatanode'.find(serverName) >= 0:
        log.warn('开始启动 {host} 节点 {serverName} 服务'.format(host=host, serverName=serverName))
        _shell = _shell + 'hadoop-daemon.sh start {serverName}"'.format(serverName=serverName)
        exeCmd.run(_shell)
    elif 'resourcemanagernodemanager'.find(serverName) >= 0:
        log.warn('开始启动 {host} 节点 {serverName} 服务'.format(host=host, serverName=serverName))
        _shell = _shell + 'yarn-daemon.sh start {serverName}"'.format(serverName=serverName)
        exeCmd.run(_shell)
    else:
        log.warn('开始启动 {host} 节点 {serverName} 服务'.format(host=host, serverName=serverName))
        _shell = _shell + 'mr-jobhistory-daemon.sh start historyserver"'
        exeCmd.run(_shell)


if __name__ == '__main__':
    exeCheckServerProcess()
