#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from setup.utils import xml_util
from setup.utils.logger import logger

log = logger()
hdfsXml = xml_util.getXml('../config/hdfs-site.xml', 'property')
