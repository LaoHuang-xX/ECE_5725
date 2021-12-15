#
# ECE 5725 final project
# RPi Robot Mover
# Fall 2021
# Authors: Xu Hai (xh357), Yaqun Niu (yn232)
#

#!/usr/bin/env python3
import socket
import time
import os
from subprocess import call

# Specify the Android phone IP and port address
HOST = '10.48.92.55'
PORT = 8080

# AF_INET is the Internet address family for IPv4
# SOCK_STREAM indicates the protocol used is TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Start to connect...")
print('HOST: ' + HOST)
print(PORT)
s.connect((HOST, PORT))
print("Connected!")

cur_dir = os.getcwd()

# Make sure mode-switch signal file has been removed
while os.path.exists(cur_dir + "/quit_manual.txt"):
    os.remove(cur_dir + "/quit_manual.txt")

time.sleep(1)

# Initial the mode flag
manual_mode = False

# Time out
start_time = time.time()

# Keep receiving data from the server
while 1:
    if (time.time() - start_time >= 300):
        break
    data = s.recv(1024)
    data = repr(data)
    tmp = data.split(' ')

    # Capture corresponding information from server raw data
    if len(tmp) > 1:
        tmp = tmp[0].split('=')[-1]

        # Manual mode
        if int(tmp) == 0:

            # First time to enter manual mode
            if not manual_mode:
                if os.path.exists(cur_dir + "/quit_manual.txt"):
                    os.remove(cur_dir + "/quit_manual.txt")
                if os.path.exists(cur_dir + "/commands.txt"):
                    os.remove(cur_dir + "/commands.txt")
                time.sleep(1)
                manual_mode = True
                command_file = open("commands.txt", "w")
                call("./start_manual.sh", shell=True)
                print('Start manual mode')

            # Writing data into the file read by the controller
            command_file.write(data)
            command_file.flush()

        # Auto mode
        elif int(tmp) == 1:
            if manual_mode:
                while os.path.exists(cur_dir + "/quit_auto.txt"):
                    os.remove(cur_dir + "/quit_auto.txt")
                time.sleep(1)

                # Quit manual mode
                # Create the signal file to stop manual mode programs
                manual_mode = False
                quit_manual = open("quit_manual.txt", "w")
                quit_manual.write("Hello")
                quit_manual.close()

                # Start auto mode programs
                call("./start_auto.sh", shell=True)
                print('Start auto mode')

        # Quit
        elif int(tmp) == 2:

            # Clear buffer files
            # Create the signal file to stop auto mode programs
            os.remove(cur_dir + "/quit_manual.txt")
            quit_auto = open("quit_auto.txt", "w")
            quit_auto.write("Hello")
            quit_auto.close()
            break
