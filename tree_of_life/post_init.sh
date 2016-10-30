#!/bin/bash
sudo su -c "echo nameserver 8.8.8.8 > /etc/resolv.conf"
sudo apt-get update
sudo apt-get -y install python3-pip rabbitmq-server
sudo pip3 install psutil pika
sudo service rabbitmq-server start
git clone -b Release1.1 http://github.com/hoonkim/rune $HOME/rune
