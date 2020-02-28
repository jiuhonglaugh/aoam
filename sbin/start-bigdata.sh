#!/usr/bin/env bash
AOAM_HOME=$(cd `dirname $0`; pwd)
if [ ! -d "$AOAO_HOME/bin" ] || [ ! -d "$AOAM_HOME/sbin" ];then
     AOAM_HOME=$(cd `dirname $0`/..; pwd)
fi
$AOAM_HOME/bin/azkaban.py
sleep 3
$AOAM_HOME/bin/elasticsearch.py
sleep 3
$AOAM_HOME/bin/flume.py
sleep 3
$AOAM_HOME/bin/hadoop.py
sleep 3
$AOAM_HOME/bin/hbase.py
sleep 3
$AOAM_HOME/bin/hive.py
sleep 3
$AOAM_HOME/bin/kafka.py
sleep 3
$AOAM_HOME/bin/logstash.py
sleep 3
$AOAM_HOME/bin/storm.py
sleep 3
$AOAM_HOME/bin/zookeeper.py
