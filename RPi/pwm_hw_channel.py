#
# ECE 5725 final project
# RPi Robot Mover
# Fall 2021
# Authors: Xu Hai (xh357), Yaqun Niu (yn232)
#

# Manual mode controller

import time
import RPi.GPIO as GPIO
import pigpio
import re
import os
import pygame.mixer

# Initialize GPIO settings
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
pi_hw=pigpio.pi()

filename="quit_manual.txt"

# Initialize flags
go_forward = False
back_ward = False
Turn_left = False
Turn_right = False
stop = True
playmusic=True

try:

    while True:

        # Check whether the use wants to switch to auto mode
        if os.path.exists(filename):
            pi_hw.hardware_PWM(13, 0, 0)
            pi_hw.hardware_PWM(12, 0, 0)
            pi_hw.stop()
            GPIO.cleanup()
            print("quit")
            quit()

        # Read commands from the server
        f = open('./commands.txt', 'r').read()
        command = f.split(' ')

        # Capture corresponding information from the server raw data
        if len(command) >= 2:
            command = command[-2].split('=')
            if len(command) > 2:
                x_value = float(command[0].split("n")[-1].split("'")[-1])
                y_value = float(command[1])
                z_value = float(command[2])
                manual_auto = int(command[3])

                # The commands is given based on the coordinate information of the accelerometer
                # Move forward
                if 2 < y_value < 7 and 7 < z_value < 10 and go_forward:
                    go_forward = False
                    back_ward = True
                    Turn_left = True
                    Turn_right = True
                    stop = True
                    print("forward")
                    pi_hw.hardware_PWM(13, 50, 1000000)
                    pi_hw.hardware_PWM(12, 50, 1000000)
                    GPIO.output(5, GPIO.HIGH)
                    GPIO.output(6, GPIO.LOW)
                    GPIO.output(22, GPIO.LOW)
                    GPIO.output(27, GPIO.HIGH)

                # Move backward
                elif 8 < y_value < 9 and z_value < -4 and back_ward:
                    go_forward = True
                    back_ward = False
                    Turn_left = True
                    Turn_right = True
                    stop = True
                    print("backward")
                    pi_hw.hardware_PWM(13, 50, 1000000)
                    pi_hw.hardware_PWM(12, 50, 1000000)
                    GPIO.output(5, GPIO.LOW)
                    GPIO.output(6, GPIO.HIGH)
                    GPIO.output(22, GPIO.HIGH)
                    GPIO.output(27, GPIO.LOW)

                # Turn left
                elif x_value > 4 and Turn_left:
                    go_forward = True
                    back_ward = True
                    Turn_left = False
                    Turn_right = True
                    stop = True
                    print("turn left")
                    pi_hw.hardware_PWM(13, 50, 500000)
                    pi_hw.hardware_PWM(12, 50, 500000)
                    GPIO.output(5, GPIO.LOW)
                    GPIO.output(6, GPIO.HIGH)
                    GPIO.output(22, GPIO.LOW)
                    GPIO.output(27, GPIO.HIGH)

                # Turn right
                elif x_value < -4 and Turn_right:
                    go_forward = True
                    back_ward = True
                    Turn_left = True
                    Turn_right = False
                    stop = True
                    print("turn right")
                    pi_hw.hardware_PWM(13, 50, 500000)
                    pi_hw.hardware_PWM(12, 50, 500000)
                    GPIO.output(5, GPIO.HIGH)
                    GPIO.output(6, GPIO.LOW)
                    GPIO.output(22, GPIO.HIGH)
                    GPIO.output(27, GPIO.LOW)

                # Stop
                elif -3.5 < x_value < 3.5 and 8 < y_value < 10 and -3 < z_value < 5 and stop:
                    
                    # In order to make it safe
                    # when the user first launch the program
                    # the user needs to first adjust the controller position
                    # to stop position to start controlling
                    if playmusic:
                        print("Ready")

                        # Play the sound to inform the user the robot is ready to go
                        os.system("omxplayer './sound/safe_rule.mp3'")
                    playmusic=False
                    print("stop")
                    go_forward = True
                    back_ward = True
                    Turn_left = True
                    Turn_right = True
                    stop = False
                    pi_hw.hardware_PWM(13, 0, 0)
                    pi_hw.hardware_PWM(12, 0, 0)
except KeyboardInterrupt:
    pass

pi_hw.stop()
GPIO.cleanup()


