#!/bin/bash

N=`openstack server list -f value | grep '^vm' | sort -r | head -n 1 | sed 's/vm//'`

openstack server list -f value | wc -l # Name sort
openstack server create --flavor default --key-name default --nic net-id=private --image xenial \
  --security-group default
IP=`openstack floating ip create public -c IP -f value`
nova floating-ip-associate vm1 $IP
ssh -oStrictHostKeyChecking=no ubuntu@$IP


# ret = check_output('ls -al /', shell=True)
# print ret
URL='http://github.com/hoonkim/rune'
#DIR='/opt/stack/rune'
DIR='/opt/stack/rune'

call('git clone -b Release1.0 ' + URL + ' ', shell=True)
#call('PWD=./rune git checkout Release1.0', shell=True)
#call('cd /opt/stack/


# known host clear
# instance create
# floating ip
# set floating ip setting
# post script

#shell code
#1번 Sentinel IP
#2번 인스턴스 UUID
