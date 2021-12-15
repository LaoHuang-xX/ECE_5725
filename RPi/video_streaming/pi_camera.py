#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# ECE 5725 final project
# RPi Robot Mover
# Fall 2021
# Authors: Xu Hai (xh357), Yaqun Niu (yn232)
#

import time
import io
import threading
import picamera
import os


class Camera(object):
    thread = None  # background thread
    frame = None  # current frame
    last_access = 0
 
    def initialize(self):
        if Camera.thread is None:
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()  # start background frame

            while self.frame is None:   # wait until the frame can be obtained
                time.sleep(0)

    def acquire_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame

    @classmethod
    def _thread(cls):
        with picamera.PiCamera() as camera:
            # setup parameters of picamera
            camera.resolution = (320, 240)
            camera.hflip = True
            camera.vflip = True
            running = True
            filename = "quit_manual.txt"


            # turn on camera
            camera.start_preview()
            time.sleep(2)

            stream = io.BytesIO()

            for a in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):

                stream.seek(0)
                cls.frame = stream.read()  # store frame

                stream.seek(0)
                stream.truncate()  # reset stream

                # If there is no client request for
                # more than 15 seconds, the thread will be closed

                if time.time() - cls.last_access > 15:
                    break

                if os.path.exists(filename) and running:
                    running = False
                    print("quit_manual")
                    camera.close()
                    quit()
        cls.thread = None
