#!/bin/bash
source /etc/admin-openrc

# Init keystone database
echo "DROP DATABASE IF EXISTS keystone" | mysql
echo "CREATE DATABASE keystone" | mysql
echo "GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'localhost' IDENTIFIED BY '$KEYSTONE_DBPASS'" | mysql
echo "GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'%' IDENTIFIED BY '$KEYSTONE_DBPASS'" | mysql

# Init glance database
echo "DROP DATABASE IF EXISTS glance" | mysql
echo "CREATE DATABASE glance" | mysql
echo "GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'localhost' IDENTIFIED BY '$GLANCE_DBPASS'" | mysql
echo "GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'%' IDENTIFIED BY '$GLANCE_DBPASS'" | mysql

# Init nova database
echo "DROP DATABASE IF EXISTS nova_api" | mysql
echo "DROP DATABASE IF EXISTS nova" | mysql
echo "CREATE DATABASE nova_api" | mysql
echo "CREATE DATABASE nova" | mysql
echo "GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'localhost' IDENTIFIED BY '$NOVA_DBPASS'" | mysql
echo "GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'%' IDENTIFIED BY '$NOVA_DBPASS'" | mysql
echo "GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'localhost' IDENTIFIED BY '$NOVA_DBPASS'" | mysql
echo "GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'%' IDENTIFIED BY '$NOVA_DBPASS'" | mysql

# Init neutron database
echo "DROP DATABASE IF EXISTS neutron" | mysql
echo "CREATE DATABASE neutron" | mysql
echo "GRANT ALL PRIVILEGES ON neutron.* TO 'neutron'@'localhost' IDENTIFIED BY '$NEUTRON_DBPASS'" | mysql
echo "GRANT ALL PRIVILEGES ON neutron.* TO 'neutron'@'%' IDENTIFIED BY '$NEUTRON_DBPASS'" | mysql
