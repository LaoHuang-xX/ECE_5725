#
# ECE 5725 final project
# RPi Robot Mover
# Fall 2021
# Authors: Xu Hai (xh357), Yaqun Niu (yn232)
#

# Auto mode controller

import cv2
import numpy as np
import color_recognize_v2
from piecamera import PieCamera
import time
import RPi.GPIO as GPIO
import pigpio
import re
import os

# Initialize GPIO settings
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
pi_hw=pigpio.pi()

# Initialize flags
go_forward = False
back_ward = False
Turn_left = False
Turn_right = False
stop = True

# Get the main color in front of the camera during the period
result=color_recognize_v2.get_hsv()

ball_color = result

# Define the hsv range of known colors
color_dist = {'red': {'Lower': np.array([0, 60, 60]), 'Upper': np.array([6, 255, 255])},
              'blue': {'Lower': np.array([100, 80, 46]), 'Upper': np.array([124, 255, 255])},
              'green': {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])},
              'orange': {'Lower': np.array([11, 43, 46]), 'Upper': np.array([34, 255, 255])},
              'black': {'Lower': np.array([0, 0, 0]), 'Upper': np.array([180, 255, 46])}
              }
camera = PieCamera()

i=0
key=-1
filename="quit_auto.txt"
while key == -1:
    ret, frame = camera.read()
    if ret:
        if frame is not None:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            inRange_hsv = cv2.inRange(hsv, color_dist[ball_color]['Lower'], color_dist[ball_color]['Upper'])
            
            # Find objects with required color
            cnts, h = cv2.findContours(inRange_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]

            # Lose the target
            if len(cnts) == 0:
                print("lost object")

                # Keep turning left or right to find the target
                if (i % 2) == 0:
                    print("turn left")

                    # Only half-speed to avoid missing the target
                    pi_hw.hardware_PWM(13, 50, 500000)
                    pi_hw.hardware_PWM(12, 50, 500000)
                    GPIO.output(5, GPIO.LOW)
                    GPIO.output(6, GPIO.HIGH)
                    GPIO.output(22, GPIO.LOW)
                    GPIO.output(27, GPIO.HIGH)
                    i += 1
                    time.sleep(1)


                else:
                    print("turn right")

                    # Only half-speed to avoid missing the target
                    pi_hw.hardware_PWM(13, 50, 500000)
                    pi_hw.hardware_PWM(12, 50, 500000)
                    GPIO.output(5, GPIO.HIGH)
                    GPIO.output(6, GPIO.LOW)
                    GPIO.output(22, GPIO.HIGH)
                    GPIO.output(27, GPIO.LOW)
                    i += 1
                    time.sleep(0.5)

            # Find satisfied objects
            else:
                # Only follow the biggest object
                c = max(cnts, key=cv2.contourArea)
                rect = cv2.minAreaRect(c)
                box = cv2.boxPoints(rect)
                area = cv2.contourArea(c)
                
                # Get the coordinate information of the target
                left_point_x = np.min(box[:, 0])
                right_point_x = np.max(box[:, 0])
                top_point_y = np.min(box[:, 1])
                bottom_point_y = np.max(box[:, 1])

                left_point_y = box[:, 1][np.where(box[:, 0] == left_point_x)][0]
                right_point_y = box[:, 1][np.where(box[:, 0] == right_point_x)][0]
                top_point_x = box[:, 0][np.where(box[:, 1] == top_point_y)][0]
                bottom_point_x = box[:, 0][np.where(box[:, 1] == bottom_point_y)][0]
                vertices = np.array(
                    [[top_point_x, top_point_y], [bottom_point_x, bottom_point_y], [left_point_x, left_point_y],
                     [right_point_x, right_point_y]])

                # Simply version of center of mass
                center = (vertices[2][0] + vertices[3][0]) / 2
                
                # Filter noise
                # Determine the distance by the area of the target
                if area > 800:

                    # Turn left
                    if center > 470:
                        go_forward = True
                        back_ward = True
                        Turn_left = False
                        Turn_right = True
                        stop = True
                        print("turn left")
                        pi_hw.hardware_PWM(13, 50, 750000)
                        pi_hw.hardware_PWM(12, 50, 750000)
                        GPIO.output(5, GPIO.LOW)
                        GPIO.output(6, GPIO.HIGH)
                        GPIO.output(22, GPIO.LOW)
                        GPIO.output(27, GPIO.HIGH)

                    # Turn right
                    elif center < 25:
                        go_forward = True
                        back_ward = True
                        Turn_left = True
                        Turn_right = False
                        stop = True
                        print("turn right")
                        pi_hw.hardware_PWM(13, 50, 750000)
                        pi_hw.hardware_PWM(12, 50, 750000)
                        GPIO.output(5, GPIO.HIGH)
                        GPIO.output(6, GPIO.LOW)
                        GPIO.output(22, GPIO.HIGH)
                        GPIO.output(27, GPIO.LOW)

                    # Too far away from the target
                    # Move forward
                    if area < 5500 and center >= 25 and center <= 470 and go_forward:
                        go_forward = False
                        back_ward = True
                        Turn_left = True
                        Turn_right = True
                        stop = True
                        print("forward")
                        pi_hw.hardware_PWM(13, 50, 750000)
                        pi_hw.hardware_PWM(12, 50, 750000)
                        GPIO.output(5, GPIO.HIGH)
                        GPIO.output(6, GPIO.LOW)
                        GPIO.output(22, GPIO.LOW)
                        GPIO.output(27, GPIO.HIGH)

                    # Stop
                    elif 5500 < area < 7500 and center >= 25 and center <= 470 and stop:
                        go_forward = True
                        back_ward = True
                        Turn_left = True
                        Turn_right = True
                        stop = False
                        print("stop")
                        pi_hw.hardware_PWM(13, 0, 0)
                        pi_hw.hardware_PWM(12, 0, 0)

                    # Too close to the target
                    # Move backward
                    elif area > 7500 and center >= 25 and center <= 470 and back_ward:
                        go_forward = True
                        back_ward = False
                        Turn_left = True
                        Turn_right = True
                        stop = True
                        print("backward")
                        pi_hw.hardware_PWM(13, 50, 750000)
                        pi_hw.hardware_PWM(12, 50, 750000)
                        GPIO.output(5, GPIO.LOW)
                        GPIO.output(6, GPIO.HIGH)
                        GPIO.output(22, GPIO.HIGH)
                        GPIO.output(27, GPIO.LOW)

    # Check whether the user wants to quit the program
    if os.path.exists(filename):
        pi_hw.hardware_PWM(13, 0, 0)
        pi_hw.hardware_PWM(12, 0, 0)
        pi_hw.stop()
        GPIO.cleanup()
        camera.close()
        quit()


pi_hw.stop()
GPIO.cleanup()

