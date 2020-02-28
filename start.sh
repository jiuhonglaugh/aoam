#! /bin/sh

echo "********************正在检测依赖**************************" 
count=0
sshpass -V >> /dev/null
if [ $? != 0 ];then
    echo -e "\033[31m 请安装sshpass \033[0m"
    count=$((${count} + 1))
else
    echo -e "\033[32m sshpass已经安装 \033[0m"
fi
ansible --version >> /dev/null
if [ $? != 0 ];then
    echo -e "\033[31m 请安装ansible \033[0m"
    count=$((${count} + 1))
else
    echo -e "\033[32m ansible已经安装 \033[0m"
fi

python3 -V >> /dev/null
if [ $? != 0 ];then
    echo -e "\033[31m 请安装python \033[0m"
    count=$((${count} + 1))
else
    echo -e "\033[32m python已经安装 \033[0m"
fi

if [ $count -gt 0 ];then
	echo -e "\033[31m 缺少 $count 个依赖，请先安装依赖 \033[0m" 
	exit 1
else
	echo -e "\033[32m 依赖检测完毕，准备安装组件..... \033[0m"
fi

count=`python3 -c 'import hosts; print(hosts.check_hosts())'`
if [ $count -gt 0 ];then
	echo -e "\033[31m hosts检测有误,请修复后才能继续 \033[0m"
	exit 1
else
	echo -e "\033[32m hosts检测完毕..... \033[0m"
fi

declare -A map=`python3 -c 'import hosts; print(hosts.get_passwd())'`
declare -a user_data=`python3 -c 'import hosts; print(hosts.get_file_data())'`

result=`python3 -c 'import hosts; print(hosts.check_ssh())'`

if [ $result -eq 1 ];then 
	echo -e "\033[35m 正在生成免密钥SSH \033[0m"
	ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa>/dev/null 2>&1
	cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
	chmod 600 ~/.ssh/authorized_keys
	for key in $(echo ${!map[*]})
	do
		sshpass -p${map[$key]} ssh-copy-id -i ~/.ssh/id_rsa.pub -o StrictHostKeyChecking=no -p22 ${user_data[2]}@$key	
        	echo "$key : ${map[$key]}"
	done
else
	echo -e "\033[32m SSH密钥已经生成 \033[0m"
fi

python3 -c 'import hosts; print(hosts.check_ansible_client())'

result=`python3 -c 'import hosts; print(hosts.make_ansible_client())'`

if [ $result -ne 0 ];then
	echo -e "\033[31m有$result 个IP验证未通过 \033[0m"
	exit
else
	echo -e "\033[32m ansible 配置验证成功... \033[0m"
fi

echo -e "\033[35m 创建目录存储shell脚本 \033[0m"
declare -a result=`python3 -c 'import hosts; print(hosts.get_file_data())'`
ansible ${result[0]} -m file -a 'path='${result[1]}' state=directory owner='${result[2]}' group='${result[3]}' mode=0777 recurse=yes'
echo -e "\033[35m 正在远程复制shell脚本 \033[0m"
ansible ${result[0]} -m copy -a "src='${result[4]}' dest='${result[1]}' mode=0777 owner='${result[2]}' group='${result[3]}' backup=no" -o -f 6
echo -e "\033[35m 执行远程shell脚本生成ssh \033[0m"
result=`python3 -c 'import hosts; print(hosts.make_ansible_ssh())'`
array=(${result// / })
len=${#array[*]}
num=${array[$len-1]}

if [ $num -ne 0 ];then
	echo "更新完毕..."
else
	echo "无需执行..."
fi

echo -e "\033[32m 正在安装JDK... \033[0m"
python3 -c 'import hosts; print(hosts.setup_jdk())'

echo -e "\033[32m 正在安装HADOOP... \033[0m"
python3 -c 'import hosts; print(hosts.setup_hadoop())'

echo -e "\033[32m 正在检测HADOOP服务... \033[0m"
python3 -c 'import hosts; print(hosts.check_hadoop())'

#source shell/source.sh

#_result=`ansible client -l ${result[0]} -m shell -a "${result[1]}/ssh.sh ${result[2]}"`
#echo $_result >> xx.txt
#通过逗号分隔IP
#IPS=${result[0]}
#array=(${IPS//,/ })
#for ip in ${array[@]}
#do
#	echo ${result[5]} ${result[2]} $ip
#	./shell/authorized_key.sh ${result[5]} ${result[2]} $ip
#	cat /home/${result[2]}/id_rsa.pub >> /home/${result[2]}/.ssh/authorized_keys
#done

#echo -e "\033[32m 同步公钥到各个子节点 \033[0m"
#ansible ${result[0]} -m copy -a "src='/home/${result[2]}/.ssh/authorized_keys' dest='/home/${result[2]}/.ssh/' owner='${result[2]}' group='${result[3]}' backup=yes" -o -f 6

