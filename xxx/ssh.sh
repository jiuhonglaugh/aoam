#! /bin/sh

username=$1
if [ -f "/home/$username/.ssh/id_rsa.pub" ];then
        echo -e "\033[35m SSH已经生成 \033[0m"
else
	echo -e "\033[35m 正在生成免密钥SSH \033[0m"
	ssh-keygen -t rsa -P '' -f /home/$username/.ssh/id_rsa>/dev/null 2>&1
fi

