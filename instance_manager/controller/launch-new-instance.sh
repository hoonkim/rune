#!/bin/bash
source /etc/admin-openrc
unset OS_TOKEN
openstack token issue

NUM=`openstack server list -c Name -f value | grep '^vm' | sort -r | head -n 1 | sed 's/vm//'`
if [ -z $NUM ]; then NUM=1; fi
openstack server create --flavor rune --key-name default --nic net-id=selfservice --image xenial --security-group default vm$NUM
IP=`openstack floating ip create provider -c floating_ip_address -f value`
nova floating-ip-associate vm1 $IP
while true; do
  STATUS=`openstack server show vm$NUM -c status -f value`
  if [ "$STATUS" == "ACTIVE" ]; then break; fi
done
while true; do
  scp -oStrictHostKeyChecking=no post_init.sh ubuntu@$IP:.
  if [ $? -ne 0 ]; then
    echo "Wait for creating instance vm$NUM..."
    sleep 5
    continue
  fi
  break
done
ssh -oStrictHostKeyChecking=no ubuntu@$IP ./post_init.sh
UUID=`openstack server show vm$NUM -c id -f value`
SENTINEL=`getent hosts controller | awk '{ print $1 }'`
scp -oStrictHostKeyChecking=no post_script.sh ubuntu@$IP:.
ssh -oStrictHostKeyChecking=no ubuntu@$IP ./post_script.sh $SENTINEL $UUID
