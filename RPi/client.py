#!/usr/bin/env python3
import socket
import time
import testRead

HOST = '10.48.79.139'
PORT = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data = 0
s.connect((HOST, PORT))
start_time = time.time()
while 1:
    if (time.time() - start_time >= 30):
        break
    data = s.recv(1024)
    testRead.a.append(data)
    print(repr(data))

# AF_INET is the Internet address family for IPv4
# SOCK_STREAM indicates the protocol used is TCP
#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#	s.connect((HOST, PORT))
#	s.sendall(b'Test')
#	data = s.recv(1024)

#print('Received', repr(data))
