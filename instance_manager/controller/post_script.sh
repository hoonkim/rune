#!/bin/bash
cd $HOME/rune/juggler
nohup python3 jugglerHandler.py $1 $2 1>$HOME/juggler.log 2>$HOME/juggler-error.log &
cd $HOME/rune/wisp
nohup python3 wisp.py 1>$HOME/wisp.log 2>$HOME/wisp-error.log &
