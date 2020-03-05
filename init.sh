#!/usr/bin/env bash

if [[ ! -d "${AOAM_HOME}"  ]];then
  echo "没有配置 AOAM_HOME 环境变量开始自动查找 AOAM_HOME "
  AOAM_HOME=$(cd `dirname $0`; pwd)
else
  echo "获取环境变量中的 AOAM_HOME 为： $AOAM_HOME "
fi
if [[ ! -d "${AOAM_HOME}/bin" ]] || [[ ! -d "${AOAM_HOME}/sbin" ]];then
  echo " $AOAM_HOME 目录下不存在 bin、sbin 目录 开始重新查找 AOAM_HOME "
  AOAM_HOME=$(cd `dirname $0`/..; pwd)
fi
/bin/echo "AOAO_HOME 为： $AOAM_HOME"

/bin/echo "赋予 ${AOAM_HOME}/bin/  目录下的 Python 脚本执行权限"
/bin/chmod +x ${AOAM_HOME}/bin/*.py
/bin/echo "赋予 ${AOAM_HOME}/sbin/ 目录下的 Shell 脚本执行权限"
/bin/chmod +x ${AOAM_HOME}/sbin/*.sh

/bin/echo "如果 $AOAM_HOME/logs  目录不存在将会被创建"
[[ ! -d "${AOAM_HOME}/logs" ]] && /bin/mkdir ${AOAM_HOME}/logs

/bin/echo "初始化 Python 脚本中的 sys.path.append 追加的模块路径"
/bin/sed -i s%/zywa/aoam%${AOAM_HOME}%g ${AOAM_HOME}/bin/*.py