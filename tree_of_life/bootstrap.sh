#!/bin/bash
apt-get -y install git vim sudo
git clone http://github.com/openstack-dev/devstack /devstack
/devstack/tools/create-stack-user.sh
chown -R stack.stack /devstack
mv /devstack /opt/stack
usermod -a -G sudo stack
usermod -a -G adm stack
sed -i -- "s/var=\$1/var=\"0000\"/g" /devstack/stack.sh
su -c "cd /opt/stack/devstack;./stack.sh" -- stack
source /devstack/openrc
source /devstack/stackrc
openstack token issue
wget https://cloud-images.ubuntu.com/xenial/current/xenial-server-cloudimg-amd64.tar.gz
tar -zxvf xenial-server-cloudimg-amd64.tar.gz
openstack flavor create --ram 512 --disk 8 default
ssh-keygen -f /opt/stack/.ssh/id_rsa -q -N ""
openstack keypair create --public-key /opt/stack/.ssh/id_rsa mykey
openstack security group rule create --proto icmp default
openstack security group rule create --proto tcp --dst-port 22 default
