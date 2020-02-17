#!/usr/bin/python3
# -*- encoding:utf-8 -*-
import subprocess as sbp


def check_call(cmd):
    code = 0
    try:
        sbp.check_call(cmd)
    except:
        print("运行: " + cmd + "命令失败")
        code = 1
    return code


'''
获取执行结果
'''


def getoutput(cmd):
    return sbp.getoutput(cmd)


'''
获取执行状态以及执行结果
'''


def getstatusgetoutput(cmd):
    return sbp.getstatusoutput(cmd)


def Popen(cmd):
    result = sbp.Popen(cmd)
