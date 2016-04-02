# coding=utf-8
# Author: Ron Smith
# Copyright ©2016 That Ain't Working, All Rights Reserved


# the ATAP value of the XBee radio. AP=2 is recommended.
ATAP = 2

START_BYTE = 0x7E
ESCAPE = 0x7D
XON = 0x11
XOFF = 0x13

# This value determines the size of the byte array for receiving RX packets
# Most users won't be dealing with packets this large so you can adjust this
# value to reduce memory consumption. But, remember that
# if a RX packet exceeds this size, it cannot be parsed!

# This value is determined by the largest packet size (100 byte payload + 64-bit address + option byte and rssi byte) of a series 1 radio
MAX_FRAME_DATA_SIZE = 110


BROADCAST_ADDRESS = 0xFFFF
ZB_BROADCAST_ADDRESS = 0xFFFE


# the non-variable length of the frame data (not including frame id or api id or variable data size
# (e.g. payload, at command set value)
ZB_TX_API_LENGTH = 12
ZB_EXPLICIT_TX_API_LENGTH = 18
TX_16_API_LENGTH = 3
TX_64_API_LENGTH = 9
AT_COMMAND_API_LENGTH = 2
REMOTE_AT_COMMAND_API_LENGTH = 13
# start/length(2)/api/frameid/checksum bytes
PACKET_OVERHEAD_LENGTH = 6
# api is always the third byte in packet
API_ID_INDEX = 3

# frame position of rssi byte
RX_16_RSSI_OFFSET = 2
RX_64_RSSI_OFFSET = 8

DEFAULT_FRAME_ID = 1
NO_RESPONSE_FRAME_ID = 0

# These are the parameters used by the XBee ZB modules when you do a
# regular "ZB TX request".
DEFAULT_ENDPOINT = 232
DEFAULT_CLUSTER_ID = 0x0011
DEFAULT_PROFILE_ID = 0xc105

# TODO put in tx16 class
ACK_OPTION = 0
DISABLE_ACK_OPTION = 1
BROADCAST_OPTION = 4

# RX options
ZB_PACKET_ACKNOWLEDGED = 0x01
ZB_BROADCAST_PACKET = 0x02

# not everything is implemented!
###
# Api Id constants
###
TX_64_REQUEST = 0x0
TX_16_REQUEST = 0x1
AT_COMMAND_REQUEST = 0x08
AT_COMMAND_QUEUE_REQUEST = 0x09
REMOTE_AT_REQUEST = 0x17
ZB_TX_REQUEST = 0x10
ZB_EXPLICIT_TX_REQUEST = 0x11
RX_64_RESPONSE = 0x80
RX_16_RESPONSE = 0x81
RX_64_IO_RESPONSE = 0x82
RX_16_IO_RESPONSE = 0x83
AT_RESPONSE = 0x88
TX_STATUS_RESPONSE = 0x89
MODEM_STATUS_RESPONSE = 0x8a
ZB_RX_RESPONSE = 0x90
ZB_EXPLICIT_RX_RESPONSE = 0x91
ZB_TX_STATUS_RESPONSE = 0x8b
ZB_IO_SAMPLE_RESPONSE = 0x92
ZB_IO_NODE_IDENTIFIER_RESPONSE = 0x95
AT_COMMAND_RESPONSE = 0x88
REMOTE_AT_COMMAND_RESPONSE = 0x97


###
# TX STATUS constants
###
SUCCESS = 0x0
CCA_FAILURE = 0x2
INVALID_DESTINATION_ENDPOINT_SUCCESS = 0x15
NETWORK_ACK_FAILURE = 0x21
NOT_JOINED_TO_NETWORK = 0x22
SELF_ADDRESSED = 0x23
ADDRESS_NOT_FOUND = 0x24
ROUTE_NOT_FOUND = 0x25
PAYLOAD_TOO_LARGE = 0x74
# Returned by XBeeWithCallbacks::waitForStatus on timeout
XBEE_WAIT_TIMEOUT = 0xff

# modem status
HARDWARE_RESET = 0
WATCHDOG_TIMER_RESET = 1
ASSOCIATED = 2
DISASSOCIATED = 3
SYNCHRONIZATION_LOST = 4
COORDINATOR_REALIGNMENT = 5
COORDINATOR_STARTED = 6

ZB_BROADCAST_RADIUS_MAX_HOPS = 0

ZB_TX_UNICAST = 0
ZB_TX_BROADCAST = 8

AT_OK = 0
AT_ERROR = 1
AT_INVALID_COMMAND = 2
AT_INVALID_PARAMETER = 3
AT_NO_RESPONSE = 4

NO_ERROR = 0
CHECKSUM_FAILURE = 1
PACKET_EXCEEDS_BYTE_ARRAY_LENGTH = 2
UNEXPECTED_START_BYTE = 3
