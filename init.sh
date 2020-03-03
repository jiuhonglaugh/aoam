#!/usr/bin/env bash
AOAM_HOME=$(cd `dirname $0`; pwd)
if [ ! -d "$AOAO_HOME/bin" ] || [ ! -d "$AOAM_HOME/sbin" ];then
     AOAM_HOME=$(cd `dirname $0`/..; pwd)
fi
/bin/echo "AOAO_HOME 为： $AOAM_HOME"

/bin/echo "赋予 $AOAM_HOME/bin/ 目录下的 Python 脚本执行权限"
/bin/chmod +x $AOAM_HOME/bin/*.py
/bin/echo "赋予 $AOAM_HOME/sbin/ 目录下的 Shell 脚本执行权限"
/bin/chmod +x $AOAM_HOME/sbin/*.sh

/bin/echo "如果 $AOAM_HOME/logs 目录不存在将会被创建"
[ ! -d "$AOAM_HOME/logs" ] && /bin/mkdir $AOAM_HOME/logs

/bin/echo "初始化 Python 脚本中的 sys.path.append 追加的模块路径"
/bin/sed -i "s#/zywa/aoam#"$AOAM_HOME"#g" $AOAM_HOME/bin/azkaban.py
/bin/sed -i "s#/zywa/aoam#"$AOAM_HOME"#g" $AOAM_HOME/bin/elasticsearch.py
/bin/sed -i "s#/zywa/aoam#"$AOAM_HOME"#g" $AOAM_HOME/bin/flume.py
/bin/sed -i "s#/zywa/aoam#"$AOAM_HOME"#g" $AOAM_HOME/bin/hadoop.py
/bin/sed -i "s#/zywa/aoam#"$AOAM_HOME"#g" $AOAM_HOME/bin/hbase.py
/bin/sed -i "s#/zywa/aoam#"$AOAM_HOME"#g" $AOAM_HOME/bin/hive.py
/bin/sed -i "s#/zywa/aoam#"$AOAM_HOME"#g" $AOAM_HOME/bin/kafka.py
/bin/sed -i "s#/zywa/aoam#"$AOAM_HOME"#g" $AOAM_HOME/bin/logstash.py
/bin/sed -i "s#/zywa/aoam#"$AOAM_HOME"#g" $AOAM_HOME/bin/storm.py
/bin/sed -i "s#/zywa/aoam#"$AOAM_HOME"#g" $AOAM_HOME/bin/tomcat.py
/bin/sed -i "s#/zywa/aoam#"$AOAM_HOME"#g" $AOAM_HOME/bin/zookeeper.py