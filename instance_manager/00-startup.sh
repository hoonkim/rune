#!/bin/bash
./01-install-packages.sh
./02-generate-admin-openrc.sh
./03-setup-openstack-environment.sh
./04-init-database.sh
./05-sync-database.sh
./06-setup-server-environment.sh
./07-bootstrap-openstack.sh
