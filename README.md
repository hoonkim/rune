# What is Rune?
--------------
Rune is an environment to make construction for server easy.  You can add API(function) on dashboard and call it through http protocol on client side you make.

Rune makes server developers happy when they start making services with Rune environment.

Enjoy flexable server environment!

# Requirements
---
OS: ubuntu 16.04 server LTS
Hardware: minimal specification like below:
  - CPU: 700 MHz processor (about Intel Celeron or better)
  - RAM: 512 MiB + (512 MiB per each vm)
  - DISK: 5 GB of hard-drive space + (10 GB per each vm)
  - NIC: 2+ nic required, one is used to connect external, other is used to manage LAN.

# How to install?
---
Rune consists of two parts, controller and compute node.

Controller node is mandatory and you can install like below step:

    $ git clone -b Release1.1 http://github.com/hoonkim/rune $BASE_DIR
    $ cd $BASE_DIR/scripts/controller
    $ sudo ./00-startup.sh

After installing controller completely, essential openstack and rune services will be run on the controller node.
You can check rune process like below:

    $ ps -ef | grep python3

    sentinel: python3 run.py 9000
    dashboard: python3 manage.py runserver 0.0.0.0:8080

If you have more server computer, you can extends optional compute node like below:

    $ git clone -b Release1.1 http://github.com/hoonkim/rune $BASE_DIR
    $ cd $BASE_DIR/scripts/compute
    $ sudo ./00-startup.sh
