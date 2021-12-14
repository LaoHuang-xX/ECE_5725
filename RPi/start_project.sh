#!/bin/bash
#
# Script to start the project
#

echo "Initialize pigpiod"
sudo pigpiod

echo "Start 'web_display.py'"
python3 /home/pi/final_project/video_streaming/web_display.py&

sleep 10

echo "Start 'client.py'"
python3 /home/pi/final_project/client.py&
