#!/usr/bin/python3
# -*- encoding:utf-8 -*-
import xml.etree.ElementTree as ET


def getXml(filePath, lable):
    tree = ET.parse(filePath)  # open
    root = tree.getroot()
    list = {}
    for student in root.iter(lable):  # Element.iter()
        list[student[0].text] = student[1].text
    return list


def getHadoopXml():
    hadoopXml = {}
    tmp = getXml('../config/hdfs-site.xml', 'property')
    hadoopXml['dfs.http.address'] = tmp.get('dfs.http.address')
    hadoopXml['dfs.namenode.secondary.http-address'] = tmp.get('dfs.namenode.secondary.http-address')

    tmp = getXml('../config/core-site.xml', 'property')
    hadoopXml['fs.defaultFS'] = tmp.get('fs.defaultFS')
    return hadoopXml


if __name__ == '__main__':
    list = getHadoopXml()
    print(list)
