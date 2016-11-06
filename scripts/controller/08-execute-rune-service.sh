#!/bin/bash
source /etc/admin-openrc
unset OS_TOKEN
openstack token issue

wget https://cloud-images.ubuntu.com/xenial/current/xenial-server-cloudimg-amd64-disk1.vmdk -O xenial.vmdk
openstack image create xenial --file xenial.vmdk --container-format bare --disk-format vmdk --public

git clone -b Release1.1 http://github.com/hoonkim/rune /rune
echo "DROP DATABASE IF EXISTS rune_dev" | mysql
echo "CREATE DATABASE rune_dev" | mysql
cat /rune/schema/sentinel.sql | mysql rune_dev
cd /rune/sentinel
nohup python3 run.py 9000 1>/var/log/sentinel.log 2>/var/log/sentinel-error.log &
cd /rune/dashboard_demo
nohup python3 manage.py runserver 0.0.0.0:8080 1>/var/log/dashboard.log 2>/var/log/dashboard-error.log &
echo "Rune services run successful"
