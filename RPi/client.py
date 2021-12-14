#!/usr/bin/env python3
import socket
import time
import os
from subprocess import call

HOST = '10.48.92.55'
PORT = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Start to connect...")
print('HOST: ' + HOST)
print(PORT)
s.connect((HOST, PORT))
print("Connected!")

cur_dir = os.getcwd()

while os.path.exists(cur_dir + "/quit_manual.txt"):
    os.remove(cur_dir + "/quit_manual.txt")

time.sleep(1)
manual_mode = False

start_time = time.time()
while 1:
    if (time.time() - start_time >= 300):
        break
    data = s.recv(1024)
    data = repr(data)
    tmp = data.split(' ')
    if len(tmp) > 1:
        tmp = tmp[0].split('=')[-1]
        if int(tmp) == 0:
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
            command_file.write(data)
            command_file.flush()
        elif int(tmp) == 1:
            if manual_mode:
                while os.path.exists(cur_dir + "/quit_auto.txt"):
                    os.remove(cur_dir + "/quit_auto.txt")
                time.sleep(1)
                manual_mode = False
                quit_manual = open("quit_manual.txt", "w")
                quit_manual.write("Hello")
                quit_manual.close()
                call("./start_auto.sh", shell=True)
                print('Start auto mode')
        elif int(tmp) == 2:
            os.remove(cur_dir + "/quit_manual.txt")
            quit_auto = open("quit_auto.txt", "w")
            quit_auto.write("Hello")
            quit_auto.close()
            break
