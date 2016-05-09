# coding=utf-8
# Created by Ron Smith on 5/8/2016
# Copyright ©2016 That Ain't Working, All Rights Reserved

from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST
from utils.data import tobytes


class UDPBroadcaster:

    def __init__(self, port):
        self.port = port
        self._socket = socket(AF_INET, SOCK_DGRAM)
        self._socket.bind(('', 0))
        self._socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    def send(self, msg):
        self._socket.sendto(tobytes(msg), ('<broadcast>', self.port))

    def close(self):
        self._socket.close()
