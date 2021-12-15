#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Video transformation

import os
import time
from time import sleep
from flask import Flask, render_template, request, Response
from pi_camera import Camera

web_page = Flask(__name__)



@web_page.route('/')
def web_display():
	# Display video streaming on web page

	templateData = {
	  'panServoAngle'	: 23,
	  'tiltServoAngle'	: 32
	}
	return render_template('video_display.html', **templateData)


def generator(camera):
	# Generate video streaming
	while True:
		frame = camera.acquire_frame()
		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@web_page.route('/video_feed')
def video_feed():

	return Response(generator(Camera()),
					mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
	web_page.run(host='0.0.0.0', port=8050) 
	# filename = "quit_manual.txt"
	# while True:
	# 	if os.path.exists(filename):
	# 		print("quit_web_display")
	# 		quit()



