#!/bin/bash

# Input controller ipv4
while true; do
  echo -n "Input Controller IPv4: "
  read CONTROLLER_IP
  echo $CONTROLLER_IP | grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}' 1>/dev/null 2>&1
  if [ $? -eq 0 ]; then
    break
  else
    echo -n "Not valid IPv4 address, "
  fi
done

# Pull openrc from controller
echo -n "Controller username: "
read CTRL_USER
echo -n "Controller password: "
read -s CTRL_PASS
sshpass -p $CTRL_PASS ssh -oStrictHostKeyChecking=no $CTRL_USER@$CONTROLLER_IP "cat /etc/admin-openrc" > /etc/admin-openrc

if [ $? -ne 0 ]; then
  echo 'Fail to pull /etc/admin-openrc fron controller'
  exit 1
fi

source /etc/admin-openrc

# Setup environment
MANAGEMENT_INTERFACE_NAME=`route -n | grep '^10\.' | head -n 1 | awk '{ print $8 }'`
MANAGEMENT_INTERFACE_IP=`ifconfig $MANAGEMENT_INTERFACE_NAME | grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}' | head -n 1`
PROVIDER_INTERFACE_NAME=`route -n | grep '^192\.168\.' | head -n 1 | awk '{ print $8 }'`
PROVIDER_INTERFACE_IP=`ifconfig $PROVIDER_INTERFACE_NAME | grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}' | head -n 1`

# Init host address
echo "$CONTROLLER_IP controller" >> /etc/hosts

# Init time server
grep -r "^server" /etc/chrony/chrony.conf

if [ $? -ne 0 ]; then
  echo server controller iburst >> /etc/chrony/chrony.conf
  service chrony restart
fi

# Init openstack
BASE_DIR=/etc
METADATA_SECRET=0000
MANAGEMENT_INTERFACE_IP_ADDRESS=$MANAGEMENT_INTERFACE_IP
PROVIDER_INTERFACE_NAME=$PROVIDER_INTERFACE_NAME
OVERLAY_INTERFACE_IP_ADDRESS=$PROVIDER_INTERFACE_IP

mkdir -p $BASE_DIR/neutron/plugins/ml2
chown -R neutron.neutron $BASE_DIR/neutron

mkdir -p $BASE_DIR/nova
chown -R nova.nova $BASE_DIR/nova

A=`cat nova/nova.conf | grep -v '^#' | grep -v '^$'`
eval echo "\"$A\"" > $BASE_DIR/nova/nova.conf

A=`cat nova/nova-compute.conf | grep -v '^#' | grep -v '^$'`
eval echo "\"$A\"" > $BASE_DIR/nova/nova-compute.conf

A=`cat neutron/neutron.conf | grep -v '^#' | grep -v '^$'`
eval echo "\"$A\"" > $BASE_DIR/neutron/neutron.conf

A=`cat neutron/plugins/ml2/linuxbridge_agent.ini | grep -v '^#' | grep -v '^$'`
eval echo "\"$A\"" > $BASE_DIR/neutron/plugins/ml2/linuxbridge_agent.ini
