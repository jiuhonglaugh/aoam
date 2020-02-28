#!/usr/bin/env bash
echo "开始启动azkaban--web服务"
base_dir=$(cd `dirname $0`; pwd)
cd $base_dir
./bin/azkaban-web-start.sh $base_dir >$base_dir/logs/web.log 2>&1 &