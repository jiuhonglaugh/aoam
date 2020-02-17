#!/usr/bin/python3
# -*- encoding:utf-8 -*-


'''
判断路径最后一位是不是 /
如果不是则添加/
'''


def repairPath(path):
    if str(path).endswith('/'):
        return path
    return path + '/'


'''
写文件,当文件不存在会自动创建
字符串写入
'''


def _writeFileLf(strOrList, path):
    if len(strOrList) > 1:
        with open(path, mode='a', encoding='utf-8') as f:
            for line in strOrList:
                f.write(line + "\n")
    else:
        with open(path, mode='a', encoding='utf-8') as f:
            f.write(strOrList + "\n")


def _writeFile(strOrList, path):
    with open(path, mode='a', encoding='utf-8') as f:
        if len(strOrList) > 1:
            with open(path, mode='a', encoding='utf-8') as f:
                for line in strOrList:
                    f.write(line)
        else:
            with open(path, mode='a', encoding='utf-8') as f:
                f.write(strOrList)


def writeFile(str, path, lf=True):
    if lf:
        _writeFileLf(str, path)
    else:
        _writeFile(str, path)
