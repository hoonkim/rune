#!/bin/bash
source /etc/admin-openrc
openstack token issue

# Init host address
grep -r "controller" /etc/hosts

if [ $? -ne 0 ]; then
  echo '127.0.0.1 controller' >> /etc/hosts
fi

# Init time server
grep -r "^server" /etc/chrony/chrony.conf

if [ $? -ne 0 ]; then
  echo server kr.pool.ntp.org iburst >> /etc/chrony/chrony.conf
fi

# Init message queue server
rabbitmqctl add_user openstack $RABBIT_PASS
rabbitmqctl set_permissions openstack ".*" ".*" ".*"

# Restart service
service apache2 restart
service glance-api restart
service glance-registry restart
service libvirt-bin restart
service mysql restart
service neutron-dhcp-agent restart
service neutron-l3-agent restart
service neutron-linuxbridge-agent restart
service neutron-metadata-agent restart
service neutron-server restart
service nova-api restart
service nova-conductor restart
service nova-consoleauth restart
service nova-novncproxy restart
service nova-scheduler restart
service rabbitmq-server restart
