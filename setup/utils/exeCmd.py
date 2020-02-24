#!/usr/bin/python3
# -*- encoding:utf-8 -*-
import sys

sys.path.append('/zywa/aoam')
import subprocess as sbp
from setup.utils.logger import logger

log = logger()


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


def execJps(host):
    return Popen('ansible client -l {host} -a "jps"'.format(host=host))


def Popen(cmd):
    result = sbp.Popen(cmd, shell=True, stdout=sbp.PIPE)
    return str(result.stdout.read(), 'utf-8')


def run(cmd):
    log.info("开始执行 {} 命令".format(cmd))
    sbp.run(cmd, shell=True)
