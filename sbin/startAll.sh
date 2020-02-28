#!/usr/bin/env bash
AOAM_HOME=$(cd `dirname $0`; pwd)
if [ -d '$AOAO_HOME/bin' ] || [ -d '$AOAM_HOME/sbin' ];then
    echo "AOAM 家目录为 $AOAM_HOME"
else
    AOAM_HOME=$(cd `dirname $0`/..; pwd)
    echo "AOAM 家目录为 $AOAM_HOME"
fi
echo "监控脚本执行时间："$(date "+%Y-%m-%d %H:%M:%S")

$AOAM_HOME/bin/start-backend.sh $AOAM_HOME
$AOAM_HOME/bin/bigdata.sh $AOAM_HOME