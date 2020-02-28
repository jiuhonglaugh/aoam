#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#scriptname:py.test.py

import subprocess
import re

def get_foo():
    return "foo"
 
def get_bar():
    return "bar"

def get_data():
	result = subprocess.run("ansible client -m ping",shell=True)
	print(result)
	sub = subprocess.Popen("ansible client -m ping", shell=True, stdout=subprocess.PIPE)
	content =str(sub.stdout.read(),'utf-8')
	fo = open("tmp.txt", "w")
	fo.write(content)
	fo.close()
	for line in open("tmp.txt","r"):
		flag = re.findall("=>",line)
		if(len(flag)>0):
			arr = line.split("=>")[0].split("|")
			if(arr[1].strip() != "SUCCESS"):
				print(arr[0],"无法通讯")



if __name__ == "__main__":
	get_data()
