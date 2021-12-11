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
try:
    while True:
        f = open('./commands.txt', 'r').read()
        command = f.split(' ')
        if len(command) >= 2:
            command = command[-2].split('=')
            if len(command) > 2:
                x_value = float(command[0].split("'")[-1])
                y_value = float(command[1])
                z_value = float(command[2])
                # time.sleep(2)

                if 3 < y_value < 5 and 8 < z_value < 10 and go_forward:
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

                elif 8 < y_value < 10 and z_value < -3 and back_ward:
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

                elif x_value > 5 and Turn_left:
                    go_forward = True
                    back_ward = True
                    Turn_left = False
                    Turn_right = True
                    stop = True
                    print("turn left")
                    pi_hw.hardware_PWM(13, 50, 1000000)
                    pi_hw.hardware_PWM(12, 50, 1000000)
                    GPIO.output(5, GPIO.LOW)
                    GPIO.output(6, GPIO.HIGH)
                    GPIO.output(22, GPIO.LOW)
                    GPIO.output(27, GPIO.HIGH)
                # time.sleep(3)

                elif x_value < -5 and Turn_right:
                    go_forward = True
                    back_ward = True
                    Turn_left = True
                    Turn_right = False
                    stop = True
                    print("turn right")
                    pi_hw.hardware_PWM(13, 50, 1000000)
                    pi_hw.hardware_PWM(12, 50, 1000000)
                    GPIO.output(5, GPIO.HIGH)
                    GPIO.output(6, GPIO.LOW)
                    GPIO.output(22, GPIO.HIGH)
                    GPIO.output(27, GPIO.LOW)
                    # time.sleep(3)

                elif -5 < x_value < 5 and 9 < y_value < 10 and -3 < z_value < 8 and stop:
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


