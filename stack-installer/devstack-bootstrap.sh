# 1: Avoid bug from commit 18d966929305f5086d5b12c404af1fee0882ed26
yes | pip uninstall pycparser

# 2: Install devstack
useradd -m stack
echo 'stack ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers
su - stack -c "git clone -b stable/mitaka \
  https://git.openstack.org/openstack-dev/devstack /home/stack/devstack"
printf 'Admin Password: '
read ADMIN_PASSWORD
export ADMIN_PASSWORD=$ADMIN_PASSWORD

echo "[[local|localrc]]
ADMIN_PASSWORD=$ADMIN_PASSWORD
DATABASE_PASSWORD=\$ADMIN_PASSWORD
RABBIT_PASSWORD=\$ADMIN_PASSWORD
SERVICE_PASSWORD=\$ADMIN_PASSWORD" > /home/stack/local.conf
chown stack.stack /home/stack/local.conf

/home/stack/devstack/tools/create-stack-user.sh 
su stack -c "cd /home/stack/devstack; ./stack.sh"

# 3: Setup admin account
sed -i -- "s/#admin_token.*$/admin_token = $ADMIN_PASSWORD/g" \
  /etc/keystone/keystone.conf
service apache2 restart
exit 0

# 4: Download 2016.9.30 released ubuntu:xenial cloud image for vm
wget http://cloud-images.ubuntu.com/xenial/20160930/xenial-server-cloudimg-amd64-disk1.img \
  -O /home/stack/xenial-server-clouding-amd64-disk1.img

for i in `ps -ef | grep '[Gg]lance' | awk '{ print $2 }'`; do kill -9 $i; done
nohup /usr/bin/python /usr/local/bin/glance-registry --config-file=/etc/glance/glance-registry.conf > /dev/null 2>&1 &
nohup /usr/bin/python /usr/local/bin/glance-api --config-file=/etc/glance/glance-api.conf > /dev/null 2>&1 &
