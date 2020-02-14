#!/usr/bin/python3
# -*- encoding:utf-8 -*-
#scriptname:py.hosts.py

import configparser
import re
import subprocess
import os
import threading
import time


'''
读取自定义hosts文件
IP和主机的映射关系
'''
config = configparser.ConfigParser()
config.read("source/hosts.ini")

'''
修改host文件，IP和域名的映射
'''
content = open("/etc/hosts","r").read()
def check_hosts():
	num = 0
	for key in config["hosts"]:
		hostname = config["hosts"][key] + " " + key
		if(len(re.findall(hostname,content))>0):
			#print("\033[32m "+hostname+"已经配置到hosts文件 \033[0m")
			pass
		else:
			num += 1
			#print("\033[31m "+hostname+"尚未配置到hosts文件 \033[0m")
			#print("\033[33m 注意：如果检测已经配置，请确认IP和域名是否为一个空格 \033[0m")
	return num

def get_passwd():
	dirs="("
	for key in config["passwd"]:
		dirs += "["+key+"]=\""+config["passwd"][key]+"\" "
	dirs += ")"
	return dirs

def check_ssh():
	user = config["username"]["user"]
	rsa = os.path.exists("/home/"+user+"/.ssh/id_rsa.pub")
	authorized = os.path.exists("/home/"+user+"/.ssh/authorized_keys")
	if rsa and authorized:
		return 0
	else:
		return 1;

'''
修改ansible的hosts配置文件
'''
def check_ansible_host():
	content=open("/etc/ansible/hosts").read()
	_ansibleclient=""
	if(len(re.findall("client",content))<1):
        	_ansibleclient="[client]\n"

	for key in config["client"]:
        	_ip = hostname=config["client"][key]
        	if(len(re.findall(_ip,content))<1):
                	_ansibleclient=_ansibleclient+_ip+"\n"
	return _ansibleclient


def check_ansible_client():
	result = subprocess.run("ansible client -m ping",shell=True)
	sub = subprocess.Popen("ansible client -m ping", shell=True, stdout=subprocess.PIPE)
	content =str(sub.stdout.read(),'utf-8')
	fo = open("tmp.txt", "w")
	fo.write(content)
	fo.close()

def make_ansible_ssh():
	line=get_file_data()
	array = line[1:len(line)-1].split(" ")
	ssh = 'ansible client -l '+array[0]+' -m shell -a "'+array[1]+'/ssh.sh '+array[2]+'"'
	result = subprocess.Popen(ssh, shell=True, stdout=subprocess.PIPE)
	content =str(result.stdout.read(),'utf-8')
	fo = open("tmp.txt", "w")
	fo.write(content)
	fo.close()
	ip=""
	num=0
	for line in open("tmp.txt","r"):
		arr=line.split("|")
		flag=re.findall("生成免密钥SSH",arr[0])
		if(len(arr)>1):
			ip=arr[0]
		elif(len(flag)>0):
			ssh="shell/authorized_key.sh "+array[5]+" "+array[2]+" "+ip
			subprocess.run(ssh,shell=True)
			ssh="cat /home/"+array[2]+"/id_rsa.pub >> /home/"+array[2]+"/.ssh/authorized_keys"
			subprocess.run(ssh,shell=True)	
			num +=1
			print("复制完成...")
	if(num>0):
		ssh="ansible "+array[0]+" -m copy -a \"src='/home/"+array[2]+"/.ssh/authorized_keys' dest='/home/"+array[2]+"/.ssh/' owner='"+array[2]+"' group='"+array[3]+"' backup=no\" -o -f 6"
		subprocess.run(ssh,shell=True)
	return num

def make_ansible_client():
	value=0
	for line in open("tmp.txt","r"):
		flag = re.findall("=>",line)
		if(len(flag)>0):
			arr = line.split("=>")[0].split("|")
			if(arr[1].strip() != "SUCCESS"):
				value += 1
	return value

def get_file_data():
	value=""
	for key in config["hosts"]:
		if(len(value)<1):
			value="("+config["hosts"][key]
		else:
			value += ","+config["hosts"][key]

	value +=" "+config["path"]["dest"]+" "+config["username"]["user"]+" "+config["username"]["group"]+" "+config["path"]["src"]+" "+config["path"]["passwd"]+" "+config["path"]["master"]+")"
	return value

def setup_jdk():
	_source=get_file_data()
	_source=_source[1:len(_source)-1].split(" ")
	out = subprocess.getoutput("java -version")
	print("输出内容：",len(re.findall("java version",out)))
	if(len(re.findall("java version",out))<1):
		_setup=config["setuppath"]["jdk_setup_path"]
		_soft=config["softpath"]["jdk_path"]
		_base=os.path.dirname(_soft)
		_old_list=os.listdir(_base)
		_base_path=config["basepath"]["setuppath"]
		_setup_jdk_path=config["setuppath"]["jdk_setup_path"]
		print(_setup_jdk_path)
		if(os.path.exists(_setup)):
			print("jdk已经解压")
		else:
			subprocess.run("tar -zxvf "+_soft+" -C "+_base,shell=True)
			_new_list=os.listdir(_base)
			_jdk=_setup_jdk_path.split("/")[len(_setup_jdk_path.split("/"))-1]
			_jdk_soft_path=_base+"/"+_jdk
			for ip in _source[0].split(","):
				_ssh="scp -r "+_jdk_soft_path+" "+_source[2]+"@"+ip+":"+_base_path
				subprocess.run(_ssh,shell=True)
			if(len(_jdk_soft_path)>0):
				subprocess.run("rm -rf "+_jdk_soft_path,shell=True)
		
		content = open("/home/"+_source[2]+"/.bashrc","r").read()		
		if(len(re.findall("JAVA_HOME",content))<1):
			_line="echo 'export JAVA_HOME="+_setup_jdk_path+"\nexport PATH=$PATH:$JAVA_HOME/bin' >>~/.bashrc"
			subprocess.run(_line,shell=True)
		else:
			print("JDK环境变量已经配置")
		_ssh="source shell/source.sh "+_source[2]
		subprocess.run(_ssh,shell=True)
	else:
        	print("JDK已经安装：",out)

	

def check(v):
	return '([key1]="value1" [key2]="value2" [key3]="value3")'

def setup_hadoop():
	out = subprocess.getoutput("hadoop version")
	fo = open("tmp.txt", "w")
	fo.write(out)
	fo.close()
	_version=""
	_num=0
	for line in open("tmp.txt","r"):
		_num +=1
		if(len(_version)<1):
			_version=line
	if(_num>1):
		print("当前Hadoop版本：",_version)
	else:
		_source=get_file_data()
		_source=_source[1:len(_source)-1].split(" ")
		_soft=config["softpath"]["hadoop_path"]
		_base=os.path.dirname(_soft)
		_old_list=os.listdir(_base)
		_base_path=config["basepath"]["setuppath"]
		_setup_hadoop_path=config["setuppath"]["hadoop_setup_path"]
		if(os.path.exists(_setup_hadoop_path)):
			print("Hadoop已经解压")
		else:
			subprocess.run("tar -zxvf "+_soft+" -C "+_base,shell=True)
			_new_list=os.listdir(_base)
			_hadoop=_setup_hadoop_path.split("/")[len(_setup_hadoop_path.split("/"))-1]
			_hadoop_soft_path=_base+"/"+_hadoop
			_base_path=config["basepath"]["setuppath"]
			_setup_hadoop_path=config["setuppath"]["hadoop_setup_path"]
			for ip in _source[0].split(","):
				_ssh="scp -r "+_hadoop_soft_path+" "+_source[2]+"@"+ip+":"+_base_path
				subprocess.run(_ssh,shell=True)
			if(len(_hadoop_soft_path)>0):
				subprocess.run("rm -rf "+_hadoop_soft_path,shell=True)

		if(len(re.findall("HADOOP_HOME",content))<1):
			_var=["export HADOOP_HOME=/zywa/setup/hadoop-2.9.0","export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin","export LIB_NATIVE_DIR=$HADOOP_HOME/lib/native:$LD_LIBRARY_PATH","export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop"]
			_line="echo '"+"\n".join(_var)+"' >>~/.bashrc"
			subprocess.run(_line,shell=True)
		else:
			print("Hadoop环境变量已经配置..")
		_ssh="source shell/source.sh "+_source[2]
		subprocess.run(_ssh,shell=True)

def source_pro():
	line=get_file_data()
	array = line[1:len(line)-1].split(" ")
	ssh="ansible "+array[0]+" -m copy -a \"src='/home/"+array[2]+"/.bashrc' dest='/home/"+array[2]+"/' owner='"+array[2]+"' group='"+array[3]+"' backup=no\" -o -f 6"
	subprocess.run(ssh,shell=True)
	subprocess.run('ansible client -m shell -a "source /home/'+array[2]+'/.bashrc" -f 3',shell=True)

def check_hadoop():
	master=config["master"]
	for key in master:
		ip = config["master"][key]
		result = subprocess.Popen('ansible client -l '+ip+' -a "jps"', shell=True, stdout=subprocess.PIPE)
		content =str(result.stdout.read(),'utf-8')
		#服务列表
		values = config["service"][key]
		print(ip+":")
		for name in values.split("|"):
			if(len(re.findall(name,content))<1):
				start_hadoop(ip,name.lower())
			else:
				print(name+"服务正在运行")
		print("\n")

def start_hadoop(ip,name):
	HADOOP_HOME=config["setuppath"]["hadoop_setup_path"]
	if(name=="secondarynamenode" or name=="namenode" or name=="datanode"):
		_shell='ansible client -l '+ip+' -a "'+HADOOP_HOME+'/sbin/hadoop-daemon.sh start '+name+'"'
		subprocess.run(_shell,shell=True)
	elif(name=="resourcemanager" or name=="nodemanager"):
		_shell='ansible client -l '+ip+' -a "'+HADOOP_HOME+'/sbin/yarn-daemon.sh start '+name+'"'
		subprocess.run(_shell,shell=True)

def job():
	print("\033[35m 内存使用情况监测 \033[0m")
	
	_shell='ansible client -a "free -h"'
	subprocess.run(_shell,shell=True)
	print("\033[35m 磁盘使用情况监测 \033[0m")
	_shell='ansible client -a "df -lh"'
	subprocess.run(_shell,shell=True)
	print("\033[35m CPU使用负载监测 \033[0m")
	_shell="ansible client -a 'uptime'"
	subprocess.run(_shell,shell=True)
	print("\033[35m 服务检测 \033[0m")
	check_hadoop()

def run():
	while 1:
		job()
		time.sleep(10)
'''
	scheduler = BlockingScheduler()
	scheduler.add_job(job,"cron",day_of_week="0-6",minute="*")
	scheduler.start()
'''
if __name__ == "__main__":
	run()
	#check_hadoop()
	#start_hadoop("172.10.22.56","secondarynamenode")
	#source_pro()
	#setup_hadoop()
	#setup_jdk()
	#make_ansible_ssh()
	#make_ansible_client()
	#num = check_ssh()
	#print(num)
	#print(check("xxx"))
	#$get_hosts()
	#pass




