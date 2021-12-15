#!/bin/bash

#
# ECE 5725 final project
# RPi Robot Mover
# Fall 2021
# Authors: Xu Hai (xh357), Yaqun Niu (yn232)
#

#
# Script to start the project
#

echo "Initialize pigpiod"
sudo pigpiod

echo "Start 'web_display.py'"
python3 /home/pi/final_project/video_streaming/web_display.py&

# Leave enough time to finish video transformation
sleep 10

echo "Start 'client.py'"
python3 /home/pi/final_project/client.py&
