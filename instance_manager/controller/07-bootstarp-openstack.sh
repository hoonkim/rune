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

openstack flavor create --vcpus 2 --ram 512 --disk 10 rune
openstack keypair create --public-key /rune/ssh/id_rsa.pub mykey
openstack keypair list

for i in `openstack security group list -c ID -f value`; do
  openstack security group rule create --proto icmp $i
  openstack security group rule create --proto tcp --dst-port 22 $i
done

INTERFACE=`route -n | grep '192.168.' | head -n 1 | awk '{ print $8 }'`
SUBNET=`ifconfig $INTERFACE | grep 'inet addr' | grep -Eo '([0-9]{1,3}\.){2}[0-9]{1,3}' | head -n 1`

neutron net-create --shared --provider:network_type flat --provider:physical_network provider provider
neutron subnet-create --name provider --allocation-pool start=$SUBNET.150,end=$SUBNET.200 \
  --dns-nameserver 8.8.8.8 --gateway $SUBNET.1 provider $SUBNET.0/24
neutron net-create selfservice
neutron subnet-create --name selfservice --allocation-pool start=172.16.1.2,end=172.16.1.253 \
  --dns-nameserver 8.8.8.8 --gateway 172.16.1.1 selfservice 172.16.1.0/24
neutron net-update provider --router:external
neutron router-create router
neutron router-interface-add router selfservice
neutron router-gateway-set router provider
