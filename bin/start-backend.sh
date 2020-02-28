#!/usr/bin/env bash
AOAM_HOME=$(cd `dirname $0`; pwd)
if [ -d '$AOAO_HOME/bin' ] || [ -d '$AOAM_HOME/sbin' ];then
    echo "AOAM 家目录为 $AOAM_HOME"
else
    AOAM_HOME=$(cd `dirname $0`/..; pwd)
    echo "AOAM 家目录为 $AOAM_HOME"
fi
if [ -f '$AOAM_HOME/bcakend/tomcat.py' ];then
    $AOAM_HOME/bcakend/tomcat.py
else
    echo "$AOAM_HOME/bcakend/tomcat.py 文件不存在"
fi