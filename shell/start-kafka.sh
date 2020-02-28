#!/usr/bin/env bash
echo "开始启动KAFKA服务"
base_dir=$(cd `dirname $0`; pwd)
cd $base_dir
KAFKA_HOME=/zywa/kafka/kafka_2.11-0.10.2.0
num=`jps -m | grep 'config/server1' | wc -l`
echo $num
if [ "$num" != "1" ];then
    echo "启动kafka server1"
    $KAFKA_HOME/bin/kafka-server-start.sh -daemon $KAFKA_HOME/config/server1.properties
fi
num=`jps -m | grep 'config/server2' | wc -l`
if [ "$num" != "1" ];then
    echo "启动kafka server2"
    $KAFKA_HOME/bin/kafka-server-start.sh -daemon $KAFKA_HOME/config/server2.properties
fi
