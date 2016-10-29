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
sed -i -- 's/^ec2.*//g' /etc/nova/nova.conf
sed -i -- 's/ec2,//g' /etc/nova/nova.conf
sed -i -- 's/^virt_type.*/virt_type=qemu/g' /etc/nova/nova-compute.conf

METADATA_SECRET=0000

sed -i -- "s/^#nova_metadata_ip =.*/nova_metadata_ip = controller/g" /etc/neutron/metadata_agent.ini
sed -i -- "s/^#metadata_proxy_shared_secret =.*/metadata_proxy_shared_secret = $METADATA_SECRET/g" /etc/neutron/metadata_agent.ini

# /etc/nova/nova.conf

echo "
[neutron]

auth_type = password
auth_url = http://controller:35357
password = $NEUTRON_PASS
project_domain_name = default
project_name = service
region_name = RegionOne
url = http://controller:9696
user_domain_name = default
username = neutron

service_metadata_proxy = True
metadata_proxy_shared_secret = $METADATA_SECRET" >> /etc/nova/nova.conf

# /etc/neutron/plugins/ml2/linuxbridge_agent.ini

PROVIDER_INTERFACE_NAME=`route -n | head -n 3 | tail -n 1 | awk '{ print $8 }'`
OVERLAY_INTERFACE_IP_ADDRESS=`ifconfig $PROVIDER_INTERFACE_NAME | head -n 2 | tail -n 1 | grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' | head -n 1`

sed -i -- "s/^#physical_interface_mappings.*/physical_interface_mappings = provider:$PROVIDER_INTERFACE_NAME/g" /etc/neutron/plugins/ml2/linuxbridge_agent.ini
sed -i -- "s/^#enable_vxlan.*/enable_vxlan = True/g" /etc/neutron/plugins/ml2/linuxbridge_agent.ini
sed -i -- "s/^#enable_security_group.*/enable_security_group = True/g" /etc/neutron/plugins/ml2/linuxbridge_agent.ini
sed -i -- "s/^#firewall_driver.*/firewall_driver = neutron.agent.linux.iptables_firewall.IptablesFirewallDriver/g" /etc/neutron/plugins/ml2/linuxbridge_agent.ini

# /etc/neutron/neutron.conf 

## [database]

sed -i -- "s/^connection.*/connection = mysql+pymysql:\/\/neutron:$NEUTRON_DBPASS@controller\/neutron/g" /etc/neutron/neutron.conf
sed -i -- "s/^#allow_overlapping_ips.*/allow_overlapping_ips = true/g" /etc/neutron/neutron.conf

## [DEFAULT]

sed -i -- "s/^\[DEFAULT\]$/[DEFAULT]\nauth_strategy = keystone\nnotify_nova_on_port_data_changes = True\nnotify_nova_on_port_status_changes = True\nrpc_backend = rabbit\nservice_plugins = router\n/g" /etc/neutron/neutron.conf

## [oslo_messaging_rabbit]

sed -i -- "s/^\[oslo_messaging_rabbit\]$/[oslo_messaging_rabbit]\nrabbit_host = controller\nrabbit_userid = openstack\nrabbit_password = $RABBIT_PASS\n/g" /etc/neutron/neutron.conf

## [keystone_authtoken]

sed -i -- "s/^\[keystone_authtoken\]$/[keystone_authtoken]\nauth_type = password\nauth_uri = http:\/\/controller:5000\nauth_url = http:\/\/controller:35357\nmemcached_servers = controller:11211\npassword = $NEUTRON_PASS\nproject_domain_name = default\nproject_name = service\nuser_domain_name = default\nusername = neutron\n/g" /etc/neutron/neutron.conf

## [nova]

sed -i -- "s/^\[nova\]$/[nova]\nauth_type = password\nauth_url = http:\/\/controller:35357\npassword = $NOVA_PASS\nproject_domain_name = default\nproject_name = service\nregion_name = RegionOne\nuser_domain_name = default\nusername = nova\n/g" /etc/neutron/neutron.conf

# /etc/neutron/plugins/ml2/ml2_conf.ini

## [ml2]

sed -i -- "s/^\[ml2\]/[ml2]\nextension_drivers = port_security\nmechanism_drivers = linuxbridge\ntenant_network_types =\ntype_drivers = flat,vlan,vxlan,local\n/g" /etc/neutron/plugins/ml2/ml2_conf.ini

## [ml2_type_flat]

sed -i -- "s/^#flat_networks.*/flat_networks = provider/g" /etc/neutron/plugins/ml2/ml2_conf.ini

## [ml2_type_vxlan]

sed -i -- "s/^#vni_ranges.*/vni_ranges = 1:1000/g" /etc/neutron/plugins/ml2/ml2_conf.ini

## [securitygroup]

sed -i -- "s/^#enable_ipset.*/enable_ipset = True/g" /etc/neutron/plugins/ml2/ml2_conf.ini

# /etc/neutron/plugins/ml2/linuxbridge_agent.ini

## [linux_bridge]

sed -i -- "s/^#physical_interface_mappings.*/physical_interface_mappings = provider:$PROVIDER_INTERFACE_NAME/g" /etc/neutron/plugins/ml2/linuxbridge_agent.ini

## [vxlan]

sed -i -- "s/^#enable_vxlan.*/enable_vxlan = True/g" /etc/neutron/plugins/ml2/linuxbridge_agent.ini

## [securitygroup]

sed -i -- "s/^#enable_security_group.*/enable_security_group = True/g" /etc/neutron/plugins/ml2/linuxbridge_agent.ini
sed -i -- "s/^#firewall_driver.*/firewall_driver = neutron.agent.linux.iptables_firewall.IptablesFirewallDriver/g" /etc/neutron/plugins/ml2/linuxbridge_agent.ini

# /etc/neutron/dhcp_agent.ini

## [DEFAULT]

sed -i -- "s/^#dhcp_driver.*/dhcp_driver = neutron.agent.linux.dhcp.Dnsmasq/g" /etc/neutron/dhcp_agent.ini
sed -i -- "s/^#enable_isolated_metadata.*/enable_isolated_metadata = True/g" /etc/neutron/dhcp_agent.ini
sed -i -- "s/^#interface_driver.*/interface_driver = neutron.agent.linux.interface.BridgeInterfaceDriver/g" /etc/neutron/dhcp_agent.ini
