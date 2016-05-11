# coding=utf-8
# Author: Ron Smith
# Copyright ©2016 That Ain't Working, All Rights Reserved

import os

XBEE_SERIAL_PORT = os.environ.get('XBEE_SERIAL_PORT', '/dev/ttyAMA0')

XBEE_SERIAL_CONFIG = (XBEE_SERIAL_PORT, 9600, 8, 'N', 1)

WEB_SERVICE_PORT = 50001

BROADCAST_PORT = 50002
