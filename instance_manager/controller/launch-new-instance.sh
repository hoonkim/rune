#!/bin/bash
source /etc/admin-openrc
unset OS_TOKEN
openstack token issue

NUM=`openstack server list -c Name -f value | grep '^vm' | sort -r | head -n 1 | sed 's/vm//'`
if [ -z $NUM ]; then NUM=0; fi
NUM=$((NUM+1))
openstack server create --flavor rune --key-name mykey --nic net-id=selfservice --image xenial --security-group default vm$NUM
while true; do
  STATUS=`openstack server show vm$NUM -c status -f value`
  if [ "$STATUS" == "ACTIVE" ]; then
    break
  elif [ "$STATUS" == "ERROR" ]; then
     echo "Failed to create instance vm$NUM"
     exit 1
  else
    echo "Wait for starting instance vm$NUM..."
  fi
done
IP=`openstack ip floating create provider -c ip -f value`
nova floating-ip-associate vm$NUM $IP
while true; do
  scp -i /ssh/id_rsa -oStrictHostKeyChecking=no post_init.sh ubuntu@$IP:.
  if [ $? -ne 0 ]; then
    echo "Wait for booting instance vm$NUM..."
    sleep 5
    continue
  fi
  break
done
ssh -i /ssh/id_rsa -oStrictHostKeyChecking=no ubuntu@$IP ./post_init.sh
UUID=`openstack server show vm$NUM -c id -f value`
SENTINEL=`getent hosts controller | awk '{ print $1 }'`
scp -i /ssh/id_rsa -oStrictHostKeyChecking=no post_script.sh ubuntu@$IP:.
ssh -i /ssh/id_rsa -oStrictHostKeyChecking=no ubuntu@$IP ./post_script.sh $SENTINEL $UUID
