#!/bin/bash
source /etc/admin-openrc

# keystone
echo "manual" > /etc/init/keystone.override
sed -i -- "s/^#admin_token.*$/admin_token = $ADMIN_PASS/g" /etc/keystone/keystone.conf
sed -i -- "s/^connection =.*$/connection = mysql+pymysql:\/\/keystone:$KEYSTONE_DBPASS@controller\/keystone/g" /etc/keystone/keystone.conf
sed -i -- 's/^#provider.*$/provider = fernet/g' /etc/keystone/keystone.conf

# Setup glance-api.conf

## [database]
sed -i -- 's/^\(sqlite_db.*\)/#\1/g' /etc/glance/glance-api.conf
sed -i -- "s/^#connection =.*/connection = mysql+pymysql:\/\/glance:$GLANCE_DBPASS@controller\/glance/g" /etc/glance/glance-api.conf
sed -i -- "s/^#auth_uri =.*/auth_uri = http:\/\/controller:5000\nauth_url = http:\/\/controller:35357/g" /etc/glance/glance-api.conf
sed -i -- "s/^#memcached_servers =.*/memcached_servers = controller:11211/g" /etc/glance/glance-api.conf

## [keystone_authtoken]
sed -i -- "s/^#auth_type =.*/auth_type = password\nproject_domain_name = default\nuser_domain_name = default\nproject_name = service\nusername = glance\npassword = $GLANCE_PASS/g" /etc/glance/glance-api.conf

## [paste_deploy]
sed -i -- "s/^#flavor =.*/flavor = keystone/g" /etc/glance/glance-api.conf

## [glance store]
sed -i -- "s/^#stores =.*/stores = file,http/g" /etc/glance/glance-api.conf
sed -i -- "s/^#default_store =.*/default_store = file/g" /etc/glance/glance-api.conf
sed -i -- "s/^#filesystem_store_datadir =.*/filesystem_store_datadir = \/var\/lib\/glance\/images\//g" /etc/glance/glance-api.conf

# Setup glance-registry.conf

## [database]
sed -i -- 's/^\(sqlite_db.*\)/#\1/g' /etc/glance/glance-registry.conf
sed -i -- "s/^#connection =.*/connection = mysql+pymysql:\/\/glance:$GLANCE_DBPASS@controller\/glance/g" /etc/glance/glance-registry.conf

## [keystone_authtoken]
sed -i -- "s/^#auth_uri =.*/auth_uri = http:\/\/controller:5000\nauth_url = http:\/\/controller:35357/g" /etc/glance/glance-registry.conf
sed -i -- "s/^#memcached_servers =.*/memcached_servers = controller:11211/g" /etc/glance/glance-registry.conf
sed -i -- "s/^#auth_type =.*/auth_type = password\nproject_domain_name = default\nuser_domain_name = default\nproject_name = service\nusername = glance\npassword = $GLANCE_PASS/g" /etc/glance/glance-registry.conf

## [paste_deploy]
sed -i -- "s/^#flavor =.*/flavor = keystone/g" /etc/glance/glance-registry.conf

# Setup configuration
echo "
auth_strategy = keystone
firewall_driver = nova.virt.firewall.NoopFirewallDriver
my_ip = 0.0.0.0
rpc_backend = rabbit
use_neutron = True

[api_database]
connection = mysql+pymysql://nova:$NOVA_DBPASS@controller/nova_api

[database]
connection = mysql+pymysql://nova:$NOVA_DBPASS@controller/nova

[oslo_messaging_rabbit]

rabbit_host = controller
rabbit_userid = openstack
rabbit_password = $RABBIT_PASS

[keystone_authtoken]
auth_uri = http://controller:5000
auth_url = http://controller:35357
memcached_servers = controller:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = nova
password = $NOVA_PASS

[vnc]
enabled = True
vncserver_listen = \$my_ip
vncserver_proxyclient_address = \$my_ip
novncproxy_base_url = http://controller:6080/vnc_auto.html

[glance]
api_servers = http://controller:9292

[oslo_concurrency]
lock_path = /var/lib/nova/tmp" >> /etc/nova/nova.conf

METADATA_SECRET=0000

sed -i -- "s/^#nova_metadata_ip =.*/nova_metadata_ip = controller/g" /etc/neutron/metadata_agent.ini
sed -i -- "s/^#metadata_proxy_shared_secret =.*/metadata_proxy_shared_secret = $METADATA_SECRET/g" /etc/neutron/metadata_agent.ini

echo "
[neutron]
url = http://controller:9696
auth_url = http://controller:35357
auth_type = password
project_domain_name = default
user_domain_name = default
region_name = RegionOne
project_name = service
username = neutron
password = $NEUTRON_PASS

service_metadata_proxy = True
metadata_proxy_shared_secret = $METADATA_SECRET" >> /etc/nova/nova.conf

sed -i -- "s/^\[DEFAULT\]/[DEFAULT]\n\nallow_overlapping_ips = True\nauth_strategy = keystone\ncore_plugin = ml2\nrpc_backend = rabbit\nservice_plugins =\nnotify_nova_on_port_status_changes = True\nnotify_nova_on_port_data_changes = True\n/g" /etc/neutron/neutron.conf
sed -i -- "s/^connection =.*/connection = mysql+pymysql:\/\/neutron:$NEUTRON_DBPASS@controller\/neutron\n/g" /etc/neutron/neutron.conf
sed -i -- "s/^\[oslo_messaging_rabbit\]/[oslo_messaging_rabbit]\n\nrabbit_host = controller\nrabbit_userid = openstack\nrabbit_password = $RABBIT_PASS\n/g" /etc/neutron/neutron.conf
sed -i -- "s/^\[keystone_authtoken\]/[keystone_authtoken]\n\nauth_uri = http:\/\/controller:5000\nauth_url = http:\/\/controller:35357\nmemcached_servers = controller:11211\nauth_type = password\nproject_domain_name = default\nuser_domain_name = default\nproject_name = service\nusername = neutron\npassword = $NEUTRON_PASS/g" /etc/neutron/neutron.conf
sed -i -- "s/^\[nova\]/[nova]\n\nauth_url = http:\/\/controller:35357\nauth_type = password\nproject_domain_name = default\nuser_domain_name = default\nregion_name = RegionOne\nproject_name = service\nusername = nova\npassword = $NOVA_PASS\n/g" /etc/neutron/neutron.conf

# /etc/neutron/plugins/ml2/ml2_conf.ini
echo 2
sed -i -- "s/\[ml2\]/[ml2]\n\ntype_drivers = flat,vlan,vxlan\ntenant_network_types = vxlan\nmechanism_drivers = linuxbridge,l2population\nextension_drivers = port_security\n/g" /etc/neutron/plugins/ml2/ml2_conf.ini
sed -i -- "s/\[ml2_type_flat\]/[ml2_type_flat]\n\nflat_networks = provider\nvni_ranges = 1:1000\nenable_ipset = True\n/g" /etc/neutron/plugins/ml2/ml2_conf.ini
sed -i -- "s/\[securitygroup\]/[securitygroup]\n\nenable_ipset = True\n/g" /etc/neutron/plugins/ml2/ml2_conf.ini

PROVIDER_INTERFACE_NAME=`route -n | head -n 3 | tail -n 1 | awk '{ print $8 }'`
OVERLAY_INTERFACE_IP_ADDRESS=`ifconfig $PROVIDER_INTERFACE_NAME | head -n 2 | tail -n 1 | grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' | head -n 1`

sed -i -- "s/\[linux_bridge\]/[linux_bridge]\n\nphysical_interface_mappings = provider:$PROVIDER_INTERFACE_NAME\n/g" /etc/neutron/plugins/ml2/linuxbridge_agent.ini
sed -i -- "s/\[vxlan\]/[vxlan]\n\nenable_vxlan = True\nlocal_ip = $OVERLAY_INTERFACE_IP_ADDRESS\nl2_population = True\n/g" /etc/neutron/plugins/ml2/linuxbridge_agent.ini
sed -i -- "s/\[securitygroup\]/[securitygroup]\n\nenable_security_group = True\nfirewall_driver = neutron.agent.linux.iptables_firewall.IptablesFirewallDriver\n/g" /etc/neutron/plugins/ml2/linuxbridge_agent.ini

sed -i -- "s/\[DEFAULT\]/[DEFAULT]\n\ninterface_driver = neutron.agent.linux.interface.BridgeInterfaceDriver\nexternal_network_bridge =\n/g" /etc/neutron/l3_agent.ini
sed -i -- "s/\[DEFAULT\]/[DEFAULT]\n\ninterface_driver = neutron.agent.linux.interface.BridgeInterfaceDriver\ndhcp_driver = neutron.agent.linux.dhcp.Dnsmasq\nenable_isolated_metadata = True\n/g" /etc/neutron/dhcp_agent.ini
sed -i -- "s/^\/.*//g" /etc/neutron/dhcp_agent.ini
