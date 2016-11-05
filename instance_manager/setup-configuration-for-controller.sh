#!/bin/bash
source /etc/admin-openrc

# Init host address
grep -r "controller" /etc/hosts

if [ $? -ne 0 ]; then
  echo '192.168.122.101 controller' >> /etc/hosts
fi

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

# Init openstack
BASE_DIR=/etc
NET_DEV=`route -n | head -n 3 | tail -n 1 | awk '{ print $8 }'`
IP=`ifconfig $NET_DEV | head -n 2 | tail -n 1 | grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' | head -n 1`
METADATA_SECRET=$ADMIN_PASS

MANAGEMENT_INTERFACE_IP_ADDRESS=10.100.1.101
PROVIDER_INTERFACE_NAME=ens3
OVERLAY_INTERFACE_IP_ADDRESS=192.168.122.101

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
