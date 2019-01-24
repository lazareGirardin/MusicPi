#!/bin/bash
source /etc/musicPi/venv/bin/activate
cd /home/pi/MusicPi
nohup python3 musicPi.py > /dev/null 2>&1
