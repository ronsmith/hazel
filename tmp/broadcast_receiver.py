# coding=utf-8
# Created by Ron Smith on 5/7/2016
# Copyright ©2016 That Ain't Working, All Rights Reserved

# Receive UDP packets transmitted by a broadcasting service

import sys
from socket import *

MYPORT = 50000

s = socket(AF_INET, SOCK_DGRAM)
s.bind(('', MYPORT))

while 1:
    data, wherefrom = s.recvfrom(1500, 0)
    print(data, wherefrom)
