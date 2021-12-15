#
# ECE 5725 final project
# RPi Robot Mover
# Fall 2021
# Authors: Xu Hai (xh357), Yaqun Niu (yn232)
#


# Test version to use face recognition
# But the efficiency of the face recognition is too low
# Further optimization needed

import os
import cv2
import colorList
import io
import time
import threading
import numpy as np
from piecamera import PieCamera
import pygame.mixer
#import face_recognition
import pathlib as path

known_face_encodings = []

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
    result_1 = "None"
    i = 0
    same_color = True
    
    check = 0

    # Face Recognition
    #load_faces()

    #while face_recog(camera):
        #check += 1
        #if check == 2:
            #pygame.mixer.music.load(os.getcwd() + "/sound/fail.wav")
            #pygame.mixer.music.play(-1)
            #time.sleep(2)
            #pygame.mixer.music.stop()
            #quit()

    while key == -1:
        ret, frame = camera.read()
        if ret is True and same_color:
            result = get_color(frame)
            if result == result_1:
                i += 1
                if i >= 50:
                    same_color = False
                    print(result)
                    break
            else:
                i = 0
            result_1 = result

    return result

'''
# Load known faces
def load_faces():
    p = path.Path(os.getcwd() + "/reg_usr")
    global known_face_encodings
    known_face_encodings = []
    for f in p.glob('*.jpg'):
        usr_image = face_recognition.load_image_file(str(f))
        if len(face_recognition.face_encodings(usr_image)) > 0:
            usr_face_encoding = face_recognition.face_encodings(usr_image)[0]
            known_face_encodings.append(usr_face_encoding)


# Recognize faces
def face_recog(camera):
    global known_face_encodings
    lock = True

    # Get a reference to webcam #0 (the default one)
    video_capture = camera

    process_this_frame = True

    check = 0
    start_time = time.time()

    while True:
        if time.time() - start_time >= 5:
            lock = True
            break
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    check += 1
                    break
                else:
                    check = 0
        if check == 1:
            lock = False
            break
        process_this_frame = not process_this_frame
    return lock
'''
