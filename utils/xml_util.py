#!/usr/bin/python3
# -*- encoding:utf-8 -*-
import xml.etree.ElementTree as ET
from utils import file_util

def getXml(fileName, lable):
    filePath = file_util.getConfigPath() + '/{fileName}'.format(fileName=fileName)
    tree = ET.parse(filePath)  # open
    root = tree.getroot()
    list = {}
    for student in root.iter(lable):  # Element.iter()
        list[student[0].text] = student[1].text
    return list
