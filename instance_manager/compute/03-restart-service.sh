#!/bin/bash
service chrony restart
service libvirt-bin restart
service neutron-linuxbridge-agent restart
service nova-compute restart
