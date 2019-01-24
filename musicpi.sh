#!/bin/bash
source /etc/musicPi/venv/bin/activate
cd /home/pi/musicData
nohup python3 musicPi.py > /dev/null 2>&1
