import time
import RPi.GPIO as GPIO
import pigpio
import re
import os
import pygame.mixer

GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
pi_hw=pigpio.pi()
filename="quit_manual.txt"
go_forward = False
back_ward = False
Turn_left = False
Turn_right = False
stop = True
playmusic=True

try:

    while True:
        if os.path.exists(filename):
            pi_hw.hardware_PWM(13, 0, 0)
            pi_hw.hardware_PWM(12, 0, 0)
            pi_hw.stop()
            GPIO.cleanup()
            print("quit")
            quit()
        f = open('./commands.txt', 'r').read()
        command = f.split(' ')
        if len(command) >= 2:
            command = command[-2].split('=')
            if len(command) > 2:
                x_value = float(command[0].split("n")[-1].split("'")[-1])
                y_value = float(command[1])
                z_value = float(command[2])
                manual_auto = int(command[3])
               #print(x_value,y_value,z_value,command[3])
                # time.sleep(2)

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
                    # time.sleep(5)

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
                    # time.sleep(5)

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
                # time.sleep(3)

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
                    # time.sleep(3)

                elif -3.5 < x_value < 3.5 and 8 < y_value < 10 and -3 < z_value < 5 and stop:
                    if playmusic:
                        print("Ready")
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
                    # time.sleep(1)
except KeyboardInterrupt:
    pass

pi_hw.stop()
GPIO.cleanup()


