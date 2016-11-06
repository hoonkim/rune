#!/bin/bash
source /etc/admin-openrc

MANAGEMENT_INTERFACE_NAME=`route -n | grep '^10\.' | head -n 1 | awk '{ print $8 }'`
MANAGEMENT_INTERFACE_IP=`ifconfig $MANAGEMENT_INTERFACE_NAME | grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}' | head -n 1`
PROVIDER_INTERFACE_NAME=`route -n | grep '^192\.168\.' | head -n 1 | awk '{ print $8 }'`
PROVIDER_INTERFACE_IP=`ifconfig $PROVIDER_INTERFACE_NAME | grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}' | head -n 1`

# Init host address
echo "127.0.0.1 controller" >> /etc/hosts

# Init web server
echo "ServerName controller" >> /etc/apache2/apache2.conf
cp wsgi-keystone.conf /etc/apache2/sites-available
ln -s /etc/apache2/sites-available/wsgi-keystone.conf /etc/apache2/sites-enabled
service apache2 restart

# Init time server
grep -r "^server" /etc/chrony/chrony.conf

if [ $? -ne 0 ]; then
  echo server kr.pool.ntp.org iburst >> /etc/chrony/chrony.conf
  service chrony restart
fi

# Init database
sed -i -- 's/utf8mb4/utf8/g' /etc/mysql/mariadb.conf.d/*
service mysql restart

# Init message queue server
service rabbitmq-server restart
rabbitmqctl add_user openstack $RABBIT_PASS
rabbitmqctl set_permissions openstack ".*" ".*" ".*"

# Init make key
mkdir -p $HOME/.ssh
ssh-keygen -f $HOME/.ssh/id_rsa -q -N ""
chown -R $UID.$UID $HOME/.ssh

# Init openstack
BASE_DIR=/etc
METADATA_SECRET=0000
MANAGEMENT_INTERFACE_IP_ADDRESS=$MANAGEMENT_INTERFACE_IP
PROVIDER_INTERFACE_NAME=$PROVIDER_INTERFACE_NAME
OVERLAY_INTERFACE_IP_ADDRESS=$PROVIDER_INTERFACE_IP

mkdir -p $BASE_DIR/glance
chown -R glance.glance $BASE_DIR/glance

mkdir -p $BASE_DIR/keystone
chown -R keystone.keystone $BASE_DIR/keystone

mkdir -p $BASE_DIR/neutron/plugins/ml2
chown -R neutron.neutron $BASE_DIR/neutron

mkdir -p $BASE_DIR/nova
chown -R nova.nova $BASE_DIR/nova

A=`cat keystone/keystone.conf | grep -v '^#' | grep -v '^$'`
eval echo "\"$A\"" > $BASE_DIR/keystone/keystone.conf

A=`cat glance/glance-api.conf | grep -v '^#' | grep -v '^$'`
eval echo "\"$A\"" > $BASE_DIR/glance/glance-api.conf

A=`cat glance/glance-registry.conf | grep -v '^#' | grep -v '^$'`
eval echo "\"$A\"" > $BASE_DIR/glance/glance-registry.conf

A=`cat nova/nova.conf | grep -v '^#' | grep -v '^$'`
eval echo "\"$A\"" > $BASE_DIR/nova/nova.conf

A=`cat nova/nova-compute.conf | grep -v '^#' | grep -v '^$'`
eval echo "\"$A\"" > $BASE_DIR/nova/nova-compute.conf

A=`cat neutron/neutron.conf | grep -v '^#' | grep -v '^$'`
eval echo "\"$A\"" > $BASE_DIR/neutron/neutron.conf

A=`cat neutron/metadata_agent.ini | grep -v '^#' | grep -v '^$'`
eval echo "\"$A\"" > $BASE_DIR/neutron/metadata_agent.ini

A=`cat neutron/plugins/ml2/ml2_conf.ini | grep -v '^#' | grep -v '^$'`
eval echo "\"$A\"" > $BASE_DIR/neutron/plugins/ml2/ml2_conf.ini

A=`cat neutron/plugins/ml2/linuxbridge_agent.ini | grep -v '^#' | grep -v '^$'`
eval echo "\"$A\"" > $BASE_DIR/neutron/plugins/ml2/linuxbridge_agent.ini

A=`cat neutron/l3_agent.ini | grep -v '^#' | grep -v '^$'`
eval echo "\"$A\"" > $BASE_DIR/neutron/l3_agent.ini

A=`cat neutron/dhcp_agent.ini | grep -v '^#' | grep -v '^$'`
eval echo "\"$A\"" > $BASE_DIR/neutron/dhcp_agent.ini
