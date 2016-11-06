#!/bin/bash
./01-install-packages.sh
./02-generate-admin-openrc.sh
./03-setup-configuration.sh
./04-init-database.sh
./05-sync-database.sh
./06-restart-service.sh
./07-bootstarp-openstack.sh
