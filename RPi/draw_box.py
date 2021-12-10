import cv2
import numpy as np
import matplotlib

ball_color = 'orange'

color_dist = {'red': {'Lower': np.array([0, 60, 60]), 'Upper': np.array([6, 255, 255])},
              'blue': {'Lower': np.array([100, 80, 46]), 'Upper': np.array([124, 255, 255])},
              'green': {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])},
              'orange': {'Lower': np.array([11, 43, 46]), 'Upper': np.array([34, 255, 255])},
              }

cap = cv2.VideoCapture(0)
cv2.namedWindow('camera', cv2.WINDOW_AUTOSIZE)

while True:
    ret, frame = cap.read()
    if ret:
        if frame is not None:
            # gs_frame = cv2.GaussianBlur(frame, (5, 5), 0)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # erode_hsv = cv2.erode(hsv, None, iterations=2)
            # dilate_hsv=cv2.dilate(erode_hsv, None, iterations=2)
            inRange_hsv = cv2.inRange(hsv, color_dist[ball_color]['Lower'], color_dist[ball_color]['Upper'])
            cnts, h = cv2.findContours(inRange_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(cnts) == 0:
                print("lost object")
            else:
                # print("Found")
                c = max(cnts, key=cv2.contourArea)
                rect = cv2.minAreaRect(c)
                box = cv2.boxPoints(rect)
                if cv2.contourArea(c) > 6000:
                    cv2.drawContours(frame, [np.int0(box)], -1, (0, 255, 255), 2)
                else:
                    print("No satisfied")

                cv2.imshow('camera', frame)
                if cv2.waitKey(1) and 0xFF == ord('q'):
                    quit()





