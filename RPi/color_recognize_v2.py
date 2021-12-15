#
# ECE 5725 final project
# RPi Robot Mover
# Fall 2021
# Authors: Xu Hai (xh357), Yaqun Niu (yn232)
#

import cv2
import colorList
import picamera
import io
import os
import time
import threading
import numpy as np
from piecamera import PieCamera
import pygame.mixer


# Capture the main color in front of the camera for one frame
def get_color(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    maxsum = -100
    color = None
    color_dict = colorList.getColorList()

    # Image process to get 
    for d in color_dict:
        mask = cv2.inRange(hsv, color_dict[d][0], color_dict[d][1])
        cv2.imwrite(d + '.jpg', mask)
        binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)[1]
        binary = cv2.dilate(binary, None, iterations=2)
        cnts, h = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
        sum = 0
        for c in cnts:
            sum += cv2.contourArea(c)
        if sum > maxsum:
            maxsum = sum
            color = d

    return color


# Get the hsv of the main color in front of the camera during the period
def get_hsv():
    # Load color hsv from a pre-built color list
    color_dict = colorList.getColorList()
    camera = PieCamera()
    key = -1
    result_1 = "None"
    i = 0
    same_color = True

    # Play the sound to inform the user
    # that the robot starts to capture the color
    pygame.mixer.init()
    pygame.mixer.music.load(os.getcwd() + "/sound/test.wav")
    pygame.mixer.music.play(-1)
    time.sleep(1)
    pygame.mixer.music.stop()

    # Make sure the robot get the main color during the period
    while key == -1:
        ret, frame = camera.read()
        if ret is True and same_color:
            result = get_color(frame)
            if result == result_1:
                i += 1
                if i >= 50:
                    same_color = False
                    print(result)

                    # Play the sound to inform the user
                    # that the robot has captured the color
                    pygame.mixer.music.load(os.getcwd() + "/sound/success.wav")
                    pygame.mixer.music.play(-1)
                    time.sleep(2)
                    pygame.mixer.music.stop()
                    break
            else:
                i = 0
            result_1 = result

    # Close the camera to release the resource
    camera.close()
    return result

