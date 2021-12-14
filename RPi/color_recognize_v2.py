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
capture = cv2.VideoCapture("video_5.mp4")
# capture = cv.VideoCapture(0)



# from picamera.array import PiRGBArray
# from picamera import PiCamera
# import time
# import cv2
#
# # initialize the camera and grab a reference to the raw camera capture
# camera = PiCamera()
# camera.resolution = (640, 480)
# camera.framerate = 32
# rawCapture = PiRGBArray(camera, size=(640, 480))
#
# # allow the camera to warmup
# time.sleep(0.1)
#
# # capture frames from the camera
# for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
#     # grab the raw NumPy array representing the image, then initialize the timestamp
#     # and occupied/unoccupied text
#     image = frame.array
#
#     # show the frame
#     cv2.imshow("Frame", image)
#     key = cv2.waitKey(1) & 0xFF
#
#     # clear the stream in preparation for the next frame
#     rawCapture.truncate(0)


def get_color(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    maxsum = -100
    color = None
    color_dict = colorList.getColorList()

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





def get_hsv():
    color_dict = colorList.getColorList()
    camera = PieCamera()
    key = -1
    #global result_1
    result_1="None"
    #global i
    i=0
    #global same_color
    same_color = True
    # while (True):
    pygame.mixer.init()
    pygame.mixer.music.load(os.getcwd() + "/sound/test.wav")
    pygame.mixer.music.play(-1)
    time.sleep(1)
    pygame.mixer.music.stop()
    while key == -1:
        # ret, frame = capture.read()
        ret, frame = camera.read()
        # cv2.imshow('frame', frame)
        # key = cv2.waitKey(1)
        # and result != "white" and result != "black"
        if ret is True and same_color:
            result = get_color(frame)
            if result == result_1:
                i += 1
                if i >= 50:
                    same_color = False
                    print(result)
                    pygame.mixer.music.load(os.getcwd() + "/sound/success.wav")
                    pygame.mixer.music.play(-1)
                    time.sleep(2)
                    pygame.mixer.music.stop()
                    break
            else:
                i = 0
            result_1 = result

    camera.close()
    return result





# if __name__ == '__main__':
#
#     reslt,color_list = get_hsv()
#     print(reslt)
#     print(color_list)
    # while (True):
    #     ret, frame = capture.read()
    #     # cv2.imshow("Frame",frame)
    #     if ret is True and same_color:

    # print(get_hsv())

            # if result == result_1:
            #     continue
            # print(result)
            #
            # result_1 = result

    # print(get_color(frame))





