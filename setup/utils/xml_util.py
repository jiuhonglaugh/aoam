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
