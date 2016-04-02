# coding=utf-8
# Author: Ron Smith
# Copyright ©2016 That Ain't Working, All Rights Reserved

from xbee import ZigBee
from serial import Serial
from config import XBEE_PORT, ZIGBEE_BROADCAST_LONG_ADDR, ZIGBEE_BROADCAST_SHORT_ADDR

with Serial(XBEE_PORT, 9600) as srl:
    zb = ZigBee(srl)
    zb.send('tx', data='Hello ZigBee!', dest_addr_long=ZIGBEE_BROADCAST_LONG_ADDR, dest_addr=ZIGBEE_BROADCAST_SHORT_ADDR)

