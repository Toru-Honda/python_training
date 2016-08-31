#!/usr/bin/env python
#-*- coding: utf-8 -*-

import socket as sock

HOST = '192.168.9.4'
PORT = 8080

s = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print("Connected by", addr)

while True:
    data = conn.recv(1024)
    s = "recv: "
    for d in data:
        s += str(d)
    print(s)
    if len(data) == 0:
        break
    send = data[0] + data[1] + 0x02 + 0xff + 0xff + 0x00 + 0x00
    conn.send(data)

conn.close();
