#!/usr/bin/env bash
echo "开始启动azkaban——exec服务"
base_dir=$(cd `dirname $0`; pwd)
cd $base_dir

# pass along command line arguments to azkaban-executor-start.sh script
./bin/azkaban-executor-start.sh "$@" > $base_dir/logs/exec.log 2>&1 &