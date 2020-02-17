#!/usr/bin/python3
# -*- encoding:utf-8 -*-
import xml.etree.ElementTree as ET
from setup.utils import file_util


def getXml(filePath, lable):
    tree = ET.parse(filePath)  # open
    root = tree.getroot()
    list = {}
    for student in root.iter(lable):  # Element.iter()
        list[student[0].text] = student[1].text
    return list


def getHadoopXml(configPath):
    hadoopXml = {}
    tmp = getXml(configPath + 'hdfs-site.xml', 'property')
    hadoopXml['dfs.http.address'] = tmp.get('dfs.http.address')
    hadoopXml['dfs.namenode.secondary.http-address'] = tmp.get('dfs.namenode.secondary.http-address')

    tmp = getXml(configPath + 'core-site.xml', 'property')
    hadoopXml['fs.defaultFS'] = tmp.get('fs.defaultFS')

    tmp = getXml(configPath + 'yarn-site.xml', 'property')
    hadoopXml['yarn.resourcemanager.webapp.address'] = tmp.get('yarn.resourcemanager.webapp.address')
    hadoopXml['yarn.resourcemanager.hostname'] = tmp.get('yarn.resourcemanager.hostname')
    hadoopXml['yarn.log.server.web-service.url'] = tmp.get('yarn.log.server.web-service.url')
    hadoopXml['yarn.log.server.url'] = tmp.get('yarn.log.server.url')

    tmp = getXml(configPath + 'mapred-site.xml', 'property')
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


def updateDict(olds, news):
    for old in news:
        print(old)


if __name__ == '__main__':
    print(checkServerProcess())
