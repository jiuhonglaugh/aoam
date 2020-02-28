#!/usr/bin/env bash
AOAM_HOME=$(cd `dirname $0`; pwd)
if [ ! -d '$AOAO_HOME/bin' ] || [ ! -d '$AOAM_HOME/sbin' ];then
     AOAM_HOME=$(cd `dirname $0`/..; pwd)
fi
if [ -f '$AOAM_HOME/bin/tomcat.py' ];then
    $AOAM_HOME/backend/tomcat.py
else
    echo "$AOAM_HOME/bin/tomcat.py 文件不存在"
fi