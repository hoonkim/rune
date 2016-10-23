#!/bin/bash
source /etc/admin-openrc

# Init host address
grep -r "controller" /etc/hosts

# Init web server
echo "ServerName controller" >> /etc/apache2/apache2.conf
ln -s wsgi-keystone.conf /etc/apache2/sites-enabled
service apache2 restart

if [ $? -ne 0 ]; then
  echo '127.0.0.1 controller' >> /etc/hosts
fi

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
