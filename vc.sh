#!/bin/bash
pid=$1  #获取进程pid
echo $pid
interval=1  #设置采集间隔
while true
do
    echo $(date +"%y-%m-%d %H:%M:%S") >> proc_memlog.txt
    cat  /proc/$pid/status|grep -e VmRSS >> proc_memlog.txt    #获取内存占用
    cpu=`top -n 1 -p $pid|tail -2|head -1|awk '{ssd=NF-4} {print $ssd}'`    #获取cpu占用
    echo "Cpu: " $cpu >> proc_memlog.txt
    echo $blank >> proc_memlog.txt
    sleep $interval
done
