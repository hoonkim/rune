#!/bin/bash
source /etc/admin-openrc

# Sync keystone
keystone-manage db_sync
keystone-manage fernet_setup --keystone-user keystone --keystone-group keystone

# Synchoronize glance
glance-manage db_sync

# Synchoronize database
nova-manage api_db sync
nova-manage db sync

# Sync neutron
neutron-db-manage --config-file /etc/neutron/neutron.conf --config-file /etc/neutron/plugins/ml2/ml2_conf.ini upgrade head
