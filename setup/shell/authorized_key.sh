#!/usr/bin/expect

set password [lindex $argv 0]
set username [lindex $argv 1]
set ip [lindex $argv 2]

spawn scp -r $username@$ip:/home/$username/.ssh/id_rsa.pub /home/$username
expect "Password:"
send "$password\r"
interact


