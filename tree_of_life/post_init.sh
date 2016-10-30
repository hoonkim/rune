#!/bin/bash
sudo su -c "echo nameserver 8.8.8.8 > /etc/resolv.conf"
sudo apt-get -y install python3-pip
sudo pip -y install psutil
git clone -b Release1.0 http://github.com/hoonkim/rune $HOME/rune
