# coding=utf-8
# Author: rsmith
# Copyright ©2016 That Ain't Working, All Rights Reserved

import logging

from serial import Serial
from threading import Thread
from utils import available_cpus
from .globals import *


logger = logging.getLogger(__name__)


class XBee:
    """
    Primary interface for communicating with an XBee Radio.
    This class provides methods for sending and receiving packets with an XBee radio via the serial port.
    The XBee radio must be configured in API (packet) mode (AP=2)
    in order to use this software.
    """

    def __init__(self, serial_device, baud_rate=9600):
        self._serial_device = serial_device
        self._baud_rate = baud_rate

    def read_packet(self, timeout=0):
        """
        Reads all available serial bytes until a packet is parsed or an error occurs.
        NOTE: packeet data must be read before the serial buffer overflows or data will be lost, so you must call this
              method frequently. See XBeeWithCallbacks for an implementation that takes care this for you.
        :param timeout: the number milliseconds to wait for a packet or 0 to wait indefinitely
        :return: an XBeeResponse or None
        """
        pass  # TODO

    def send(self, request):
        """
        Sends a request via the XBee radio without waiting for a response
        :param request: an XBeeRequest object or equivalent
        :return: None
        """
        pass  # TODO

    def send_and_wait(self, request, timeout=0):
        """
        Sends a request via the XBee radio then waits for a response
        :param request: an XBeeRequest
        :param timeout: the number milliseconds to wait for a response or 0 to wait indefinitely
        :return: an XBeeResponse or None
        """
        pass  # TODO


class XBeeWithCallbacks(Thread):
    """
    A class for running XBee's readPacket() in a thread and calling user-supplied callback methods when a response
    is avaiable. The callback function can expect to receive the response object as an argument.

    As a subclass of Thread, you just call the start() method to kick off the thread.
    Callbacks will be called in new thread.
    Includes a partial implementation of the XBee class to allow sending requests.
    """

    def __init__(self, serial_device, baud_rate=9600):
        super().__init__()
        self._serial_device = serial_device
        self._baud_rate = baud_rate

        self.xbee = XBee(serial_device, baud_rate)

        #callback functions
        self.on_packet_error = None
        self.on_response = None
        self.on_other_response = None
        self.on_zb_tx_status_response = None
        self.on_zb_rx_response = None
        self.on_zb_explicit_rx_response = None
        self.on_zb_rx_io_sample_response = None
        self.on_tx_status_response = None
        self.on_rx_16_response = None
        self.on_rx_64_response = None
        self.on_rx_16_io_sample_response = None
        self.on_rx_64_io_sample_response = None
        self.on_modem_status_response = None
        self.on_st_command_response = None
        self.on_remote_at_command_response = None

    def run(self):
        response = None
        while True:
            try:
                response = self.xbee.read_packet()  # no timeout, will wait indefinitely
            except Exception as ex:
                if self.on_packet_error:
                    self.on_packet_error(ex)
                    continue

            if not response:
                logger.warning("read_packet returned None. That really shouldn't happen")
                continue

            if self.on_response:
                t = Thread(target=self.on_response, args=(response,))
                t.daemon = True
                t.start()

            if response.api_id == ZB_TX_STATUS_RESPONSE:


            # TODO find a callback
