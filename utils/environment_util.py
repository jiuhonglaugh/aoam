#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os

'''
如果服务器中配置了环境变量
下面对应的不需要配置
'''


class environment_util:
    ELASTICSEARCH_HOME = None
    KAFKA_HOME = None
    HADOOP_HOME = None
    HBASE_HOME = None
    HIVE_HOME = None
    STORM_HOME = None
    JAVA_HOME = None
    ZOOKEEPER_HOME = None
    AZKABAN_HOME = None
    LOGSTATSH_HOME = None
    FLUME_HOME = None

    PREFIX_LOGS = None
    AZKABAN_LOGS = None
    LOGSTATSH_LOGS = None
    ZOOKEEPER_LOGS = None
    STORM_LOGS = None
    KAFKA_LOGS = None
    HADOOP_LOGS = None
    HBASE_LOGS = None
    FLUME_LOGS = None
    HIVE_LOGS = None
    ELASTICSEARCH_LOGS = None

    def __init__(self, PREFIX_LOGS='/zywa'):
        self.PREFIX_LOGS = PREFIX_LOGS
        self.HADOOP_LOGS = self.PREFIX_LOGS + '/hadoop'
        self.HBASE_LOGS = self.PREFIX_LOGS + '/hbase'
        self.HIVE_LOGS = self.PREFIX_LOGS + '/hive'
        self.STORM_LOGS = self.PREFIX_LOGS + '/storm'
        self.ZOOKEEPER_LOGS = self.PREFIX_LOGS + 'zookeeper'
        self.AZKABAN_LOGS = self.PREFIX_LOGS + '/azkaban'
        self.LOGSTATSH_LOGS = self.PREFIX_LOGS + '/logstatsh'
        self.KAFKA_LOGS = self.PREFIX_LOGS + '/kafka'
        self.ELASTICSEARCH_LOGS = self.PREFIX_LOGS + '/elasticsearch'
        self.FLUME_LOGS = self.PREFIX_LOGS + 'flume'
        if os.getenv('HADOOP_HOME') is not None:
            self.HADOOP_HOME = os.getenv('HADOOP_HOME')
        if os.getenv('HBASE_HOME') is not None:
            self.HBASE_HOME = os.getenv('HBASE_HOME')
        if os.getenv('HIVE_HOME') is not None:
            self.HIVE_HOME = os.getenv('HIVE_HOME')
        if os.getenv('ELASTICSEARCH_HOME') is not None:
            self.ELASTICSEARCH_HOME = os.getenv('ELASTICSEARCH_HOME')
        if os.getenv('JAVA_HOME') is not None:
            self.JAVA_HOME = os.getenv('JAVA_HOME')
        if os.getenv('KAFKA_HOME') is not None:
            self.KAFKA_HOME = os.getenv('KAFKA_HOME')
        if os.getenv('AZKABAN_HOME') is not None:
            self.AZKABAN_HOME = os.getenv('AZKABAN_HOME')
        if os.getenv('STORM_HOME') is not None:
            self.STORM_HOME = os.getenv('STORM_HOME')
        if os.getenv('LOGSTATSH_HOME') is not None:
            self.LOGSTATSH_HOME = os.getenv('LOGSTATSH_HOME')
        if os.getenv('ZOOKEEPER_HOME') is not None:
            self.ZOOKEEPER_HOME = os.getenv('ZOOKEEPER_HOME')
        if os.getenv('FLUME_HOME') is not None:
            self.FLUME_HOME = os.getenv('FLUME_HOME')


if __name__ == '__main__':
    env = environment_util()
    print(env.HADOOP_HOME)
