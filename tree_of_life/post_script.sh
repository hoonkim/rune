#!/bin/bash
cd $HOME/rune/juggler
nohup python3 jugglerHandler.py $1 $2 1>$HOME/juggler.log 2>$HOME/juggler-error.log &
