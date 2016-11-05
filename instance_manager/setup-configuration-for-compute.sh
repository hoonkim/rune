#!/bin/bash
source /etc/admin-openrc

# Init host address
grep -r "controller" /etc/hosts

if [ $? -ne 0 ]; then
  echo '192.168.122.101 controller' >> /etc/hosts
fi

# Init time server
grep -r "^server" /etc/chrony/chrony.conf

if [ $? -ne 0 ]; then
  echo server controller iburst >> /etc/chrony/chrony.conf
  service chrony restart
fi

# Init openstack
BASE_DIR=/etc
NET_DEV=`route -n | head -n 3 | tail -n 1 | awk '{ print $8 }'`
IP=`ifconfig $NET_DEV | head -n 2 | tail -n 1 | grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' | head -n 1`
METADATA_SECRET=$ADMIN_PASS

MANAGEMENT_INTERFACE_IP_ADDRESS=10.100.1.102
PROVIDER_INTERFACE_NAME=ens3
OVERLAY_INTERFACE_IP_ADDRESS=192.168.122.102

mkdir -p $BASE_DIR/neutron/plugins/ml2
chown -R neutron.neutron $BASE_DIR/neutron

mkdir -p $BASE_DIR/nova
chown -R nova.nova $BASE_DIR/nova

A=`cat nova/nova.conf.2 | grep -v '^#' | grep -v '^$'`
eval echo "\"$A\"" > $BASE_DIR/nova/nova.conf

A=`cat nova/nova-compute.conf | grep -v '^#' | grep -v '^$'`
eval echo "\"$A\"" > $BASE_DIR/nova/nova-compute.conf

A=`cat neutron/neutron.conf.2 | grep -v '^#' | grep -v '^$'`
eval echo "\"$A\"" > $BASE_DIR/neutron/neutron.conf

A=`cat neutron/plugins/ml2/linuxbridge_agent.ini.2 | grep -v '^#' | grep -v '^$'`
eval echo "\"$A\"" > $BASE_DIR/neutron/plugins/ml2/linuxbridge_agent.ini
