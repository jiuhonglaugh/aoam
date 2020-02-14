#!/bin/bash
pid=$1 #获取进程pid
echo $pid
interval=1 #设置采集间隔
while true
do
echo $(date +"%y-%m-%d %H:%M:%S") >> proc_memlog.txt
cat /proc/$pid/status|grep -e VmRSS >> proc_memlog.txt #获取内存占用
cpu=`top -b -n 1 -p $pid  2>&1 | awk -v pid=$pid '{if ($1 == pid)print $9}'` #获取cpu占用
echo "Cpu: " $cpu >> proc_memlog.txt
echo $blank >> proc_memlog.txt
sleep $interval
done


cpu_core=$(grep -c processor /proc/cpuinfo)
total_time1=$(awk '{if ($1 == "cpu") {sum = $2 + $3 + $4 + $5 + $6 + $7 + $8 + $9 + $10 + $11;print sum}}' /proc/stat)
cpu_time1=$(awk '{sum=$14 + $15;print sum}' /proc/$pid/stat)
sleep 1
total_time2=$(awk '{if ($1 == "cpu") {sum = $2 + $3 + $4 + $5 + $6 + $7 + $8 + $9 + $10 + $11;print sum}}' /proc/stat)
cpu_time2=$(awk '{sum=$14 + $15;print sum}' /proc/$pid/stat)
awk -v cpu_time1=$cpu_time1 -v total_time1=$total_time1 -v cpu_time2=$cpu_time2 -v total_time2=$total_time2 -v cpu_core=$cpu_core 'BEGIN{cpu=((cpu_time2 - cpu_time1) / (total_time2 - total_time1)) * 100*cpu_core;print cpu}'

echo $cpu_core $total_time1 $cpu_time1 $total_time2 $cpu_time2 $cpu_core

