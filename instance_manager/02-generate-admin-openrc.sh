#!/bin/bash

ADMIN_RC_PATH=/etc/admin-openrc
DEMO_RC_PATH=/etc/demo-openrc

echo "export ADMIN_PASS=`openssl rand -hex 10`" > $ADMIN_RC_PATH
echo "export CEILOMETER_DBPASS=`openssl rand -hex 10`" >> $ADMIN_RC_PATH
echo "export CEILOMETER_PASS=`openssl rand -hex 10`" >> $ADMIN_RC_PATH
echo "export CINDER_DBPASS=`openssl rand -hex 10`" >> $ADMIN_RC_PATH
echo "export CINDER_PASS=`openssl rand -hex 10`" >> $ADMIN_RC_PATH
echo "export DASH_DBPASS=`openssl rand -hex 10`" >> $ADMIN_RC_PATH
echo "export DEMO_PASS=`openssl rand -hex 10`" >> $ADMIN_RC_PATH
echo "export GLANCE_DBPASS=`openssl rand -hex 10`" >> $ADMIN_RC_PATH
echo "export GLANCE_PASS=`openssl rand -hex 10`" >> $ADMIN_RC_PATH
echo "export HEAT_DBPASS=`openssl rand -hex 10`" >> $ADMIN_RC_PATH
echo "export HEAT_DOMAIN_PASS=`openssl rand -hex 10`" >> $ADMIN_RC_PATH
echo "export HEAT_PASS=`openssl rand -hex 10`" >> $ADMIN_RC_PATH
echo "export KEYSTONE_DBPASS=`openssl rand -hex 10`" >> $ADMIN_RC_PATH
echo "export NEUTRON_DBPASS=`openssl rand -hex 10`" >> $ADMIN_RC_PATH
echo "export NEUTRON_PASS=`openssl rand -hex 10`" >> $ADMIN_RC_PATH
echo "export NOVA_DBPASS=`openssl rand -hex 10`" >> $ADMIN_RC_PATH
echo "export NOVA_PASS=`openssl rand -hex 10`" >> $ADMIN_RC_PATH
echo "export RABBIT_PASS=`openssl rand -hex 10`" >> $ADMIN_RC_PATH
echo "export SWIFT_PASS=`openssl rand -hex 10`" >> $ADMIN_RC_PATH

source $ADMIN_RC_PATH

echo "
export OS_PROJECT_DOMAIN_NAME=default
export OS_USER_DOMAIN_NAME=default
export OS_PROJECT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD=$ADMIN_PASS
export OS_AUTH_URL=http://controller:35357/v3
export OS_IDENTITY_API_VERSION=3
export OS_IMAGE_API_VERSION=2" >> $ADMIN_RC_PATH

echo "
export OS_TOKEN=$ADMIN_PASS
export OS_URL=http://controller:35357/v3
export OS_IDENTITY_API_VERSION=3" >> $ADMIN_RC_PATH

echo "export OS_PROJECT_DOMAIN_NAME=default
export OS_USER_DOMAIN_NAME=default
export OS_PROJECT_NAME=demo
export OS_USERNAME=demo
export OS_PASSWORD=$ADMIN_PASS
export OS_AUTH_URL=http://controller:5000/v3
export OS_IDENTITY_API_VERSION=3
export OS_IMAGE_API_VERSION=2" > $DEMO_RC_PATH
