#!/usr/bin/env bash
AOAM_HOME=$(cd `dirname $0`; pwd)
if [ -d '$AOAO_HOME/bin' ] || [ -d '$AOAM_HOME/sbin' ];then
    echo "AOAM 家目录为 $AOAM_HOME"
else
    AOAM_HOME=$(cd `dirname $0`/..; pwd)
    echo "AOAM 家目录为 $AOAM_HOME"
fi
$AOAM_HOME/bigdata/azkaban.py
sleep 3
$AOAM_HOME/bigdata/elasticsearch.py
sleep 3
$AOAM_HOME/bigdata/flume.py
sleep 3
$AOAM_HOME/bigdata/hadoop.py
sleep 3
$AOAM_HOME/bigdata/hbase.py
sleep 3
$AOAM_HOME/bigdata/hive.py
sleep 3
$AOAM_HOME/bigdata/kafka.py
sleep 3
$AOAM_HOME/bigdata/logstash.py
sleep 3
$AOAM_HOME/bigdata/storm.py
sleep 3
$AOAM_HOME/bigdata/zookeeper.py
