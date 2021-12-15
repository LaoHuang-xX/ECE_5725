#
# ECE 5725 final project
# RPi Robot Mover
# Fall 2021
# Authors: Xu Hai (xh357), Yaqun Niu (yn232)
#

# Face recognition function
# The efficiency is too low
# Not used in the current project
# Further optimization needed

import face_recognition
import time
import cv2
import pathlib as path
from piecamera import PieCamera


class Face:
    def __init__(self, value):
        self.lock = True
        self.usr_dir = value
        self.known_face_encodings = []

    def set_lock(self, value):
        self.lock = value

    def get_lock(self):
        return self.lock

    # Load known faces
    def load(self):
        p = path.Path(self.usr_dir)
        for f in p.glob('*.jpg'):
            usr_image = face_recognition.load_image_file(str(f))
            if len(face_recognition.face_encodings(usr_image)) > 0:
                usr_face_encoding = face_recognition.face_encodings(usr_image)[0]
                self.known_face_encodings.append(usr_face_encoding)

    # Recogniza faces
    def detect_faces(self):
        self.lock = True

        video_capture = PieCamera()

        process_this_frame = True

        check = 0
        start_time = time.time()

        while True:
            if time.time() - start_time >= 5:
                self.lock = True
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
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)

                    # If a match was found in known_face_encodings, just use the first one.
                    if True in matches:
                        check += 1
                        break
                    else:
                        check = 0
            if check == 10:
                self.lock = False
                break
            process_this_frame = not process_this_frame
        return self.lock

