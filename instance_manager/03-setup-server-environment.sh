#!/bin/bash
source /etc/admin-openrc

# Init host address
grep -r "controller" /etc/hosts

if [ $? -ne 0 ]; then
  echo '127.0.0.1 controller' >> /etc/hosts
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

PROVIDER_INTERFACE_NAME=`route -n | head -n 3 | tail -n 1 | awk '{ print $8 }'`

ovs-vsctl add-br br-provider
ovs-vsctl add-port br-provider $PROVIDER_INTERFACE_NAME
