# coding=utf-8
# Created by Ron Smith on 5/7/2016
# Copyright ©2016 That Ain't Working, All Rights Reserved

# Send UDP broadcast packets

from datetime import datetime
from time import sleep
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST

MYPORT = 50000

s = socket(AF_INET, SOCK_DGRAM)
s.bind(('', 0))
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

while 1:
    data = bytes(datetime.now().strftime('%Y-%m-%d %H:%M'), 'utf8')
    print(data)
    s.sendto(data, ('<broadcast>', MYPORT))
    sleep(60)
