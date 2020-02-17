#!/usr/bin/python3
# -*- encoding:utf-8 -*-
import xml.etree.ElementTree as ET
from setup.utils import file_util

configPath = file_util.repairPath('../config/')


def getXml(filePath, lable):
    tree = ET.parse(filePath)  # open
    root = tree.getroot()
    list = {}
    for student in root.iter(lable):  # Element.iter()
        list[student[0].text] = student[1].text
    return list


def getHadoopXml():
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
    hadoopXml['http://test:19888/jobhistory/logs'] = tmp.get('http://test:19888/jobhistory/logs')

    tmp = getXml(configPath + 'mapred-site.xml', 'property')
    hadoopXml['mapreduce.jobhistory.address'] = tmp.get('mapreduce.jobhistory.address')
    hadoopXml['mapreduce.jobhistory.webapp.address'] = tmp.get('mapreduce.jobhistory.webapp.address')

    return hadoopXml


if __name__ == '__main__':
    list = getHadoopXml()
    print(list)
