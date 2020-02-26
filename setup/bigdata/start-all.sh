#!/usr/bin/env bash
#/bin/bash
base_dir=$(cd `dirname $0`; pwd)
cd $base_dir
echo "开始运行" >> /zywa/aoam/setup/bigdata/run.log
/zywa/aoam/setup/bigdata/azkaban.py
sleep 3
/zywa/aoam/setup/bigdata/elasticsearch.py
sleep 3
/zywa/aoam/setup/bigdata/flume.py
sleep 3
/zywa/aoam/setup/bigdata/hadoop.py
sleep 3
/zywa/aoam/setup/bigdata/hbase.py
sleep 3
/zywa/aoam/setup/bigdata/hive.py
sleep 3
/zywa/aoam/setup/bigdata/kafka.py
sleep 3
/zywa/aoam/setup/bigdata/logstash.py
sleep 3
/zywa/aoam/setup/bigdata/storm.py
sleep 3
/zywa/aoam/setup/bigdata/zookeeper.py
