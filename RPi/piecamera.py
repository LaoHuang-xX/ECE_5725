import time
from picamera.array import PiRGBArray
from picamera import PiCamera


class PieCamera(PiCamera):
    def __init__(self, resolution=(480, 320), framerate=30, format='bgr', use_video_port=True, resize=None,
                 splitter_port=0, burst=False, bayer=False):
        super(PieCamera, self).__init__()
        self.resolution = resolution
        self.framerate = framerate
        self.rawCapture = PiRGBArray(self)
        time.sleep(0.1)
        self.stream = self.capture_continuous(self.rawCapture, format=format, use_video_port=use_video_port,
                                              resize=resize, splitter_port=splitter_port, burst=burst, bayer=bayer)

    def read(self):
        for frame in self.stream:
            img = frame.array
            self.rawCapture.truncate(0)
            break
        ret = True if img is not None else False
        return ret, img

    def update_attribs(self, resolution=(480, 320), framerate=30, format='bgr', use_video_port=True, resize=None,
                       splitter_port=0, burst=False, bayer=False):
        self.resolution = resolution
        self.framerate = framerate
        self.rawCapture = PiRGBArray(self, size=resolution)
        time.sleep(0.1)
        self.stream = self.capture_continuous(self.rawCapture, format=format, use_video_port=use_video_port,
                                              resize=resize, splitter_port=splitter_port, burst=burst, bayer=bayer)