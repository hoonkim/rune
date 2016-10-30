#!/bin/bash
PASS=0000
export DATABASE_PASSWORD=$PASS
export RABBIT_PASSWORD=$PASS
export SERVICE_PASSWORD=$PASS
export ADMIN_PASSWORD=$PASS
apt-get -y install git vim sudo python3-pip
yes | pip install pymysql django
git clone http://github.com/openstack-dev/devstack /devstack
/devstack/tools/create-stack-user.sh
chown -R stack.stack /devstack
mv /devstack /opt/stack
usermod -a -G sudo stack
usermod -a -G adm stack
su -c "cd /opt/stack/devstack;./stack.sh" -- stack
echo "export OS_PROJECT_NAME=admin
export OS_TENANT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD=$PASS" > /opt/stack/admin-openrc
source /opt/stack/devstack/openrc
source /opt/stack/devstack/stackrc
source /opt/stack/admin-openrc
openstack token issue
wget http://cloud-images.ubuntu.com/xenial/current/xenial-server-cloudimg-amd64-disk1.vmdk -O xenial.vmdk
openstack image create xenial --file xenial.vmdk --container-format bare --disk-format vmdk --public
openstack flavor create --ram 512 --disk 10 default
su -c "ssh-keygen -f /opt/stack/.ssh/id_rsa -q -N \"\"" -- stack
cp /opt/stack/.ssh/id_rsa $HOME/.ssh
cp /opt/stack/.ssh/id_rsa.pub $HOME/.ssh
openstack keypair create --public-key /opt/stack/.ssh/id_rsa.pub default
for i in `openstack security group list -c ID -f value`; do
  openstack security group rule create --proto icmp $i
  openstack security group rule create --proto tcp --dst-port 22 $i
done
git clone http://github.com/hoonkim/rune /rune
echo create database rune_dev | mysql -uroot -p$PASS
cat /rune/schema/sentinel.sql | mysql -uroot -p$PASS rune_dev
nohup python3 run.py 9000 1>/var/log/sentinel.log 2>/var/log/sentinel-error.log &
nohup python3 ./manage.py runserver 0.0.0.0:8080 1>/var/log/dashboard.log 2>/var/log/dashboard-error.log &
#nova floating-ip-create public
#openstack floating ip list -c "Floating IP Address" -f value
#openstack server create --flavor default --key-name mykey --nic net-id=private --image xenial --security-group default vm1
#nova floating-ip-associate vm1 172.24.4.10
