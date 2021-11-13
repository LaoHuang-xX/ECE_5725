#!/usr/bin/env python3
import socket

HOST = '10.48.101.17'
PORT = 8080

# AF_INET is the Internet address family for IPv4
# SOCK_STREAM indicates the protocol used is TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	s.sendall('Test')
	data = s.recv(1024)

print('Received', repr(data))
