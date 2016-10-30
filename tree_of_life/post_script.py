# -*- coding: utf8 -*-
import subprocess
from subprocess import call
from subprocess import check_output

URL='http://github.com/hoonkim/rune'

call('git clone -b Release1.0 ' + URL + ' /rune', shell=True)

# known host clear
# instance create
# floating ip
# set floating ip setting
# post script

#shell code
#1번 Sentinel IP
#2번 인스턴스 UUID
