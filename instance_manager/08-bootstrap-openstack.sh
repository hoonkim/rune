#!/bin/bash
source /etc/admin-openrc

openstack role add --project admin --user admin admin
openstack project create --domain default --description "Service Project" service
openstack project create --domain default --description "Demo Project" demo
openstack user create --domain default --password $ADMIN_PASS demo
openstack role create user
openstack role add --project demo --user demo user

openstack user create --domain default --password $GLANCE_PASS glance
openstack role add --project service --user glance admin
openstack service create --name glance --description "OpenStack Image" image
openstack endpoint create --region RegionOne image public http://controller:9292
openstack endpoint create --region RegionOne image internal http://controller:9292
openstack endpoint create --region RegionOne image admin http://controller:9292

openstack user create --domain default --password $NOVA_PASS nova
openstack role add --project service --user nova admin
openstack service create --name nova --description "OpenStack Compute" compute
openstack endpoint create --region RegionOne compute public http://controller:8774/v2.1/%\(tenant_id\)s
openstack endpoint create --region RegionOne compute internal http://controller:8774/v2.1/%\(tenant_id\)s
openstack endpoint create --region RegionOne compute admin http://controller:8774/v2.1/%\(tenant_id\)s

openstack user create --domain default --password $NEUTRON_PASS neutron
openstack role add --project service --user neutron admin
openstack service create --name neutron --description "OpenStack Networking" network
openstack endpoint create --region RegionOne network public http://controller:9696
openstack endpoint create --region RegionOne network internal http://controller:9696
openstack endpoint create --region RegionOne network admin http://controller:9696

unset OS_TOKEN
openstack token issue
sed -i -- 's/^export OS_TOKEN.*//g' /etc/admin-openrc

openstack flavor create --id 0 --vcpus 1 --ram 64 --disk 1 m1.nano
openstack keypair create --public-key $HOME/.ssh/id_rsa.pub mykey
openstack keypair list

openstack security group rule create --proto icmp default
openstack security group rule create --proto tcp --dst-port 22 default

exit 0

neutron net-create net1
neutron net-create net2 --provider:network-type local
neutron subnet-create net1 192.168.2.0/24 --name subnet1
neutron router-create router1

ROUTER=router1
NETWORK=net1

neutron router-gateway-set $ROUTER $NETWORK
neutron router-interface-add ROUTER SUBNET
neutron port-create net1 --fixed-ip ip_address=192.168.2.40
neutron port-create net1
neutron port-list --fixed-ips ip_address=192.168.2.2 ip_address=192.168.2.40
