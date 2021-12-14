import cv2
import numpy as np
import color_recognize_v2
from piecamera import PieCamera
import time
import RPi.GPIO as GPIO
import pigpio
import re
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
pi_hw=pigpio.pi()
go_forward = False
back_ward = False
Turn_left = False
Turn_right = False
stop = True

result=color_recognize_v2.get_hsv()

ball_color = result

color_dist = {'red': {'Lower': np.array([0, 60, 60]), 'Upper': np.array([6, 255, 255])},
              'blue': {'Lower': np.array([100, 80, 46]), 'Upper': np.array([124, 255, 255])},
              'green': {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])},
              'orange': {'Lower': np.array([11, 43, 46]), 'Upper': np.array([34, 255, 255])},
              'black': {'Lower': np.array([0, 0, 0]), 'Upper': np.array([180, 255, 46])}
              }
# filename = 'shoes12.jpg'
# frame = cv2.imread(filename)
#cap = cv2.VideoCapture(0)
#cv2.namedWindow('camera', cv2.WINDOW_AUTOSIZE)
camera = PieCamera()

i=0
key=-1
filename="quit_auto.txt"
while key == -1:
    # ret, frame = cap.read()
    ret, frame = camera.read()
    if ret:
        if frame is not None:
            # gs_frame = cv2.GaussianBlur(frame, (5, 5), 0)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # erode_hsv = cv2.erode(hsv, None, iterations=2)
            # dilate_hsv=cv2.dilate(erode_hsv, None, iterations=2)
            inRange_hsv = cv2.inRange(hsv, color_dist[ball_color]['Lower'], color_dist[ball_color]['Upper'])
            cnts, h = cv2.findContours(inRange_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]


            if len(cnts) == 0:
                print("lost object")
                if (i % 2) == 0:
                    print("turn left")
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
                    pi_hw.hardware_PWM(13, 50, 500000)
                    pi_hw.hardware_PWM(12, 50, 500000)
                    GPIO.output(5, GPIO.HIGH)
                    GPIO.output(6, GPIO.LOW)
                    GPIO.output(22, GPIO.HIGH)
                    GPIO.output(27, GPIO.LOW)
                    i += 1
                    time.sleep(0.5)

            else:
                c = max(cnts, key=cv2.contourArea)
                rect = cv2.minAreaRect(c)
                box = cv2.boxPoints(rect)
                area = cv2.contourArea(c)

                # print("Found")

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
                center = (vertices[2][0] + vertices[3][0]) / 2
                # print(box)
                # print(vertices)
                # print(vertices[2][0],vertices[3][0])
                if area > 800:
                   #cv2.drawContours(frame, [np.int0(box)], -1, (0, 255, 255), 2)
                    if center > 470: #and Turn_left:
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
                    elif center < 25:# and Turn_right:
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
                    if area < 5500 and center >= 25 and center <= 470 and go_forward:
                        go_forward = False
                        back_ward = True
                        Turn_left = True
                        Turn_right = True
                        stop = True
                        print("forward")
                       #cv2.drawContours(frame, [np.int0(box)], -1, (0, 255, 255), 2)
                        pi_hw.hardware_PWM(13, 50, 750000)
                        pi_hw.hardware_PWM(12, 50, 750000)
                        GPIO.output(5, GPIO.HIGH)
                        GPIO.output(6, GPIO.LOW)
                        GPIO.output(22, GPIO.LOW)
                        GPIO.output(27, GPIO.HIGH)

                    elif 5500 < area < 7500 and center >= 25 and center <= 470 and stop:
                        go_forward = True
                        back_ward = True
                        Turn_left = True
                        Turn_right = True
                        stop = False
                        print("stop")
                        pi_hw.hardware_PWM(13, 0, 0)
                        pi_hw.hardware_PWM(12, 0, 0)

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
    if os.path.exists(filename):
        pi_hw.hardware_PWM(13, 0, 0)
        pi_hw.hardware_PWM(12, 0, 0)
        pi_hw.stop()
        GPIO.cleanup()
        camera.close()
        quit()

'''
            cv2.imshow('camera', frame)
            if cv2.waitKey(1) and 0xFF == ord('q'):
                pi_hw.stop()
                GPIO.cleanup()
                quit()

                # else:
                #     print("No satisfied")
'''

pi_hw.stop()
GPIO.cleanup()

