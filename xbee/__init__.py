# coding=utf-8

###############################################################################
# XBee-Python
# Author: Ron Smith
# Copyright ©2016 That Ain't Working, All Rights Reserved
#
# XBee-Python is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# XBee-Python is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with XBee-Python.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################
# This is a port of XBee-Arduino which is
# Copyright ©2009 Andrew Rapp. All rights reserved.
#
# XBee-Arduino is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# XBee-Arduino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with XBee-Arduino.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################

import struct
from .globals import *


class XBeeResponse:
    """
    The super class of all XBee responses (RX packets)
    Users should never attempt to create an instance of this class; instead create an instance of a subclass
    """

    MODEM_STATUS = 0x8A
    _data_offset = 0
    _api_id = 0

    def __init__(self):
        self.frame_data = b''
        self.complete = False
        self.error_code = NO_ERROR

    def reset(self):
        """Resets the response to default values"""
        self.frame_data = b''
        self.complete = False
        self.error_code = NO_ERROR

    @property
    def frame_len(self):
        return len(self.frame_data)

    @property
    def checksum(self):
        return self.frame_data[-1]



class FrameIdResponse(XBeeResponse):
    """This class is extended by all Responses that include a frame id"""

    def __init__(self):
        super().__init__()
        self.frame_id = 0


class RxDataResponse(XBeeResponse):
    """Common functionality for both Series 1 and 2 data RX data packets"""

    def __init__(self):
        super().__init__()


    @property
    def data(self):
        """Returns the payload array"""
        return self.frame_data[self._data_offset:]



class ZBTxStatusResponse(FrameIdResponse):
    """Represents a Series 2 TX status packet"""

    _api_id = ZB_TX_STATUS_RESPONSE

    def __init__(self):
        super().__init__()

    @property
    def remote_address(self):
        return  (self.frame_data[1] << 8) + self.frame_data[2]

    @property
    def tx_retry_count(self):
        return self.frame_data[3]

    @property
    def delivery_status(self):
        return self.frame_data[4]

    @property
    def discovery_status(self):
        return self.frame_data[5]

    @property
    def isSuccess(self):
        return self.delivery_status == SUCCESS


class ZBRxResponse(RxDataResponse):
    """Represents a Series 2 RX packet"""

    _api_id = ZB_RX_RESPONSE
    _data_offset = 11

    def __init__(self, remote_address=0):
        super().__init__()

    @property
    def remote_address(self):
        return struct.unpack('>Q', self.frame_data[:8])

    @property
    def remote_address_16(self):
        return struct.unpack('>H', self.frame_data[8:10])

    @property
    def option(self):
        return self.frame_data[10]

###
# Represents a Series 2 Explicit RX packet
#
# Note: The receive these responses, set AO=1. With the default AO=0,
# you will receive ZBRxResponses, not knowing exact details.
###
class ZBExplicitRxResponse(ZBRxResponse):
    """
    Represents a Series 2 Explicit RX packet.
    Note: The receive these responses, set AO=1. With the default AO=0, you will receive ZBRxResponses, not knowing exact details.
    """

    _api_id = ZB_EXPLICIT_RX_RESPONSE
    _data_offset = 17

    def __init__(self):
        super().__init__()

    @property
    def src_endpoint(self):
        return self.frame_data[10]

    @property
    def dst_endpoint(self):
        return self.frame_data[11]

    @property
    def cluster_id(self):
        return struct.unpack('>H', self.frame_data[12:14])

    @property
    def profile_id(self):
        return struct.unpack('>H', self.frame_data[14:16])

    @property
    def option(self):
        return self.frame_data[16]


class ZBRxIoSampleResponse(ZBRxResponse):
    """Represents a Series 2 RX I/O Sample packet"""

    _api_id = ZB_IO_SAMPLE_RESPONSE

    def __init__(self):
        super().__init__()

    @property
    def digital_mask(self):
        return struct.unpack('>H', self.frame_data[12:14])

    @property
    def analog_mask(self):
        return self.frame_data[14] & 0x8f

    @property
    def contains_analog(self):
        return self.analog_mask > 0

    @property
    def contains_digital(self):
        return self.digital_mask > 0

    def analog_enabled(self, pin):
        return ((self.analog_mask >> pin) & 1) == 1

    def digital_enabled(self, pin):
        return ((self.digital_mask >> pin) & 1) == 1

    def get_analog(self, pin):
        start = 15
        if self.contains_digital:
            start += 2
        for p in range(pin):
            if self.analog_enabled(p):
                start += 2
        return struct.unpack('>H', self.frame_data[start:start+2])


class TxStatusResponse(FrameIdResponse):
    """Represents a Series 1 TX Status packet"""

    _api_id = TX_STATUS_RESPONSE

    def __init__(self):
        super().__init__()

    @property
    def status(self):
        return self.frame_data[1]

    @property
    def success(self):
        return self.status == SUCCESS


class RxResponse(RxDataResponse):
    """Represents a Series 1 RX packet"""

    def __init__(self):
        super().__init__()

    @property
    def rssi(self):
        return self.frame_data[RX_16_RSSI_OFFSET]

    @property
    def option(self):
        return self.frame_data[RX_16_RSSI_OFFSET+1]

    @property
    def address_broadcast(self):
        return (self.option & 2) == 2

    @property
    def pan_broadcast(self):
        return (self.option & 4) == 4



public:
    RxResponse();
    // remember rssi is negative but this is unsigned byte so it's up to you to convert
    uint8_t getRssi();
    uint8_t getOption();
    bool isAddressBroadcast();
    bool isPanBroadcast();
    uint8_t getDataLength();
    uint8_t getDataOffset();
    virtual uint8_t getRssiOffset() = 0;
};

###
# Represents a Series 1 16-bit address RX packet
###
class Rx16Response : public RxResponse {
public:
    Rx16Response();
    uint8_t getRssiOffset();
    uint16_t getRemoteAddress16();

    static const uint8_t API_ID = RX_16_RESPONSE;
protected:
    uint16_t _remoteAddress;
};

###
# Represents a Series 1 64-bit address RX packet
###
class Rx64Response : public RxResponse {
public:
    Rx64Response();
    uint8_t getRssiOffset();
    XBeeAddress64& getRemoteAddress64();

    static const uint8_t API_ID = RX_64_RESPONSE;
private:
    XBeeAddress64 _remoteAddress;
};

###
# Represents a Series 1 RX I/O Sample packet
###
class RxIoSampleBaseResponse : public RxResponse {
    public:
        RxIoSampleBaseResponse();
        ###
        # Returns the number of samples in this packet
        ###
        uint8_t getSampleSize();
        bool containsAnalog();
        bool containsDigital();
        ###
        # Returns true if the specified analog pin is enabled
        ###
        bool isAnalogEnabled(uint8_t pin);
        ###
        # Returns true if the specified digital pin is enabled
        ###
        bool isDigitalEnabled(uint8_t pin);
        ###
        # Returns the 10-bit analog reading of the specified pin.
        # Valid pins include ADC:0-5.  Sample index starts at 0
        ###
        uint16_t getAnalog(uint8_t pin, uint8_t sample);
        ###
        # Returns true if the specified pin is high/on.
        # Valid pins include DIO:0-8.  Sample index starts at 0
        ###
        bool isDigitalOn(uint8_t pin, uint8_t sample);
        uint8_t getSampleOffset();

        ###
        # Gets the offset of the start of the given sample.
        ###
        uint8_t getSampleStart(uint8_t sample);
    private:
};

class Rx16IoSampleResponse : public RxIoSampleBaseResponse {
public:
    Rx16IoSampleResponse();
    uint16_t getRemoteAddress16();
    uint8_t getRssiOffset();

    static const uint8_t API_ID = RX_16_IO_RESPONSE;
};

class Rx64IoSampleResponse : public RxIoSampleBaseResponse {
public:
    Rx64IoSampleResponse();
    XBeeAddress64& getRemoteAddress64();
    uint8_t getRssiOffset();

    static const uint8_t API_ID = RX_64_IO_RESPONSE;
private:
    XBeeAddress64 _remoteAddress;
};

#endif

###
# Represents a Modem Status RX packet
###
class ModemStatusResponse : public XBeeResponse {
public:
    ModemStatusResponse();
    uint8_t getStatus();

    static const uint8_t API_ID = MODEM_STATUS_RESPONSE;
};

###
# Represents an AT Command RX packet
###
class AtCommandResponse : public FrameIdResponse {
    public:
        AtCommandResponse();
        ###
        # Returns an array containing the two character command
        ###
        uint8_t* getCommand();
        ###
        # Returns the command status code.
        # Zero represents a successful command
        ###
        uint8_t getStatus();
        ###
        # Returns an array containing the command value.
        # This is only applicable to query commands.
        ###
        uint8_t* getValue();
        ###
        # Returns the length of the command value array.
        ###
        uint8_t getValueLength();
        ###
        # Returns true if status equals AT_OK
        ###
        bool isOk();

        static const uint8_t API_ID = AT_COMMAND_RESPONSE;
};

###
# Represents a Remote AT Command RX packet
###
class RemoteAtCommandResponse : public AtCommandResponse {
    public:
        RemoteAtCommandResponse();
        ###
        # Returns an array containing the two character command
        ###
        uint8_t* getCommand();
        ###
        # Returns the command status code.
        # Zero represents a successful command
        ###
        uint8_t getStatus();
        ###
        # Returns an array containing the command value.
        # This is only applicable to query commands.
        ###
        uint8_t* getValue();
        ###
        # Returns the length of the command value array.
        ###
        uint8_t getValueLength();
        ###
        # Returns the 16-bit address of the remote radio
        ###
        uint16_t getRemoteAddress16();
        ###
        # Returns the 64-bit address of the remote radio
        ###
        XBeeAddress64& getRemoteAddress64();
        ###
        # Returns true if command was successful
        ###
        bool isOk();

        static const uint8_t API_ID = REMOTE_AT_COMMAND_RESPONSE;
    private:
        XBeeAddress64 _remoteAddress64;
};


###
# Super class of all XBee requests (TX packets)
# Users should never create an instance of this class; instead use an subclass of this class
# It is recommended to reuse Subclasses of the class to conserve memory
# <p/>
# This class allocates a buffer to
###
class XBeeRequest {
public:
    ###
    # Constructor
    # TODO make protected
    ###
    XBeeRequest(uint8_t apiId, uint8_t frameId);
    ###
    # Sets the frame id.  Must be between 1 and 255 inclusive to get a TX status response.
    ###
    void setFrameId(uint8_t frameId);
    ###
    # Returns the frame id
    ###
    uint8_t getFrameId();
    ###
    # Returns the API id
    ###
    uint8_t getApiId();
    // setting = 0 makes this a pure virtual function, meaning the subclass must implement, like abstract in java
    ###
    # Starting after the frame id (pos = 0) and up to but not including the checksum
    # Note: Unlike Digi's definition of the frame data, this does not start with the API ID.
    # The reason for this is the API ID and Frame ID are common to all requests, whereas my definition of
    # frame data is only the API specific data.
    ###
    virtual uint8_t getFrameData(uint8_t pos) = 0;
    ###
    # Returns the size of the api frame (not including frame id or api id or checksum).
    ###
    virtual uint8_t getFrameDataLength() = 0;
    //void reset();
protected:
    void setApiId(uint8_t apiId);
private:
    uint8_t _apiId;
    uint8_t _frameId;
};

// TODO add reset/clear method since responses are often reused
###
# Primary interface for communicating with an XBee Radio.
# This class provides methods for sending and receiving packets with an XBee radio via the serial port.
# The XBee radio must be configured in API (packet) mode (AP=2)
# in order to use this software.
# <p/>
# Since this code is designed to run on a microcontroller, with only one thread, you are responsible for reading the
# data off the serial buffer in a timely manner.  This involves a call to a variant of readPacket(...).
# If your serial port is receiving data faster than you are reading, you can expect to lose packets.
# Arduino only has a 128 byte serial buffer so it can easily overflow if two or more packets arrive
# without a call to readPacket(...)
# <p/>
# In order to conserve resources, this class only supports storing one response packet in memory at a time.
# This means that you must fully consume the packet prior to calling readPacket(...), because calling
# readPacket(...) overwrites the previous response.
# <p/>
# This class creates an array of size MAX_FRAME_DATA_SIZE for storing the response packet.  You may want
# to adjust this value to conserve memory.
#
# \author Andrew Rapp
###
class XBee {
public:
    XBee();
    ###
    # Reads all available serial bytes until a packet is parsed, an error occurs, or the buffer is empty.
    # You may call <i>xbee</i>.getResponse().isAvailable() after calling this method to determine if
    # a packet is ready, or <i>xbee</i>.getResponse().isError() to determine if
    # a error occurred.
    # <p/>
    # This method should always return quickly since it does not wait for serial data to arrive.
    # You will want to use this method if you are doing other timely stuff in your loop, where
    # a delay would cause problems.
    # NOTE: calling this method resets the current response, so make sure you first consume the
    # current response
    ###
    void readPacket();
    ###
    # Waits a maximum of <i>timeout</i> milliseconds for a response packet before timing out; returns true if packet is read.
    # Returns false if timeout or error occurs.
    ###
    bool readPacket(int timeout);
    ###
    # Reads until a packet is received or an error occurs.
    # Caution: use this carefully since if you don't get a response, your Arduino code will hang on this
    # call forever!! often it's better to use a timeout: readPacket(int)
    ###
    void readPacketUntilAvailable();
    ###
    # Starts the serial connection on the specified serial port
    ###
    void begin(Stream &serial);
    void getResponse(XBeeResponse &response);
    ###
    # Returns a reference to the current response
    # Note: once readPacket is called again this response will be overwritten!
    ###
    XBeeResponse& getResponse();
    ###
    # Sends a XBeeRequest (TX packet) out the serial port
    ###
    void send(XBeeRequest &request);
    //uint8_t sendAndWaitForResponse(XBeeRequest &request, int timeout);
    ###
    # Returns a sequential frame id between 1 and 255
    ###
    uint8_t getNextFrameId();
    ###
    # Specify the serial port.  Only relevant for Arduinos that support multiple serial ports (e.g. Mega)
    ###
    void setSerial(Stream &serial);
private:
    bool available();
    uint8_t read();
    void flush();
    void write(uint8_t val);
    void sendByte(uint8_t b, bool escape);
    void resetResponse();
    XBeeResponse _response;
    bool _escape;
    // current packet position for response.  just a state variable for packet parsing and has no relevance for the response otherwise
    uint8_t _pos;
    // last byte read
    uint8_t b;
    uint8_t _checksumTotal;
    uint8_t _nextFrameId;
    // buffer for incoming RX packets.  holds only the api specific frame data, starting after the api id byte and prior to checksum
    uint8_t _responseFrameData[MAX_FRAME_DATA_SIZE];
    Stream* _serial;
};


###
# This class can be used instead of the XBee class and allows
# user-specified callback functions to be called when responses are
# received, simplifying the processing code and reducing boilerplate.
#
# To use it, first register your callback functions using the onXxx
# methods. Each method has a uintptr_t data argument, that can be used to
# pass arbitrary data to the callback (useful when using the same
# function for multiple callbacks, or have a generic function that can
# behave differently in different circumstances). Supplying the data
# parameter is optional, but the callback must always accept it (just
# ignore it if it's unused). The uintptr_t type is an integer type
# guaranteed to be big enough to fit a pointer (it is 16-bit on AVR,
# 32-bit on ARM), so it can also be used to store a pointer to access
# more data if required (using proper casts).
#
# There can be only one callback of each type registered at one time,
# so registering callback overwrites any previously registered one. To
# unregister a callback, pass NULL as the function.
#
# To ensure that the callbacks are actually called, call the loop()
# method regularly (in your loop() function, for example). This takes
# care of calling readPacket() and getResponse() other methods on the
# XBee class, so there is no need to do so directly (though it should
# not mess with this class if you do, it would only mean some callbacks
# aren't called).
#
# Inside callbacks, you should generally not be blocking / waiting.
# Since callbacks can be called from inside waitFor() and friends, a
# callback that doesn't return quickly can mess up the waitFor()
# timeout.
#
# Sending packets is not a problem inside a callback, but avoid
# receiving a packet (e.g. calling readPacket(), loop() or waitFor()
# and friends) inside a callback (since that would overwrite the
# current response, messing up any pending callbacks and waitFor() etc.
# methods already running).
###
class XBeeWithCallbacks : public XBee {
public:

    ###
    # Register a packet error callback. It is called whenever an
    # error occurs in the packet reading process. Arguments to the
    # callback will be the error code (as returned by
    # XBeeResponse::getErrorCode()) and the data parameter.  while
    # registering the callback.
    ###
    void onPacketError(void (*func)(uint8_t, uintptr_t), uintptr_t data = 0) { _onPacketError.set(func, data); }

    ###
    # Register a response received callback. It is called whenever
    # a response was succesfully received, before a response
    # specific callback (or onOtherResponse) below is called.
    #
    # Arguments to the callback will be the received response and
    # the data parameter passed while registering the callback.
    ###
    void onResponse(void (*func)(XBeeResponse&, uintptr_t), uintptr_t data = 0) { _onResponse.set(func, data); }

    ###
    # Register an other response received callback. It is called
    # whenever a response was succesfully received, but no response
    # specific callback was registered using the functions below
    # (after the onResponse callback is called).
    #
    # Arguments to the callback will be the received response and
    # the data parameter passed while registering the callback.
    ###
    void onOtherResponse(void (*func)(XBeeResponse&, uintptr_t), uintptr_t data = 0) { _onOtherResponse.set(func, data); }

    // These functions register a response specific callback. They
    // are called whenever a response of the appropriate type was
    // succesfully received (after the onResponse callback is
    // called).
    //
    // Arguments to the callback will be the received response
    // (already converted to the appropriate type) and the data
    // parameter passed while registering the callback.
    void onZBTxStatusResponse(void (*func)(ZBTxStatusResponse&, uintptr_t), uintptr_t data = 0) { _onZBTxStatusResponse.set(func, data); }
    void onZBRxResponse(void (*func)(ZBRxResponse&, uintptr_t), uintptr_t data = 0) { _onZBRxResponse.set(func, data); }
    void onZBExplicitRxResponse(void (*func)(ZBExplicitRxResponse&, uintptr_t), uintptr_t data = 0) { _onZBExplicitRxResponse.set(func, data); }
    void onZBRxIoSampleResponse(void (*func)(ZBRxIoSampleResponse&, uintptr_t), uintptr_t data = 0) { _onZBRxIoSampleResponse.set(func, data); }
    void onTxStatusResponse(void (*func)(TxStatusResponse&, uintptr_t), uintptr_t data = 0) { _onTxStatusResponse.set(func, data); }
    void onRx16Response(void (*func)(Rx16Response&, uintptr_t), uintptr_t data = 0) { _onRx16Response.set(func, data); }
    void onRx64Response(void (*func)(Rx64Response&, uintptr_t), uintptr_t data = 0) { _onRx64Response.set(func, data); }
    void onRx16IoSampleResponse(void (*func)(Rx16IoSampleResponse&, uintptr_t), uintptr_t data = 0) { _onRx16IoSampleResponse.set(func, data); }
    void onRx64IoSampleResponse(void (*func)(Rx64IoSampleResponse&, uintptr_t), uintptr_t data = 0) { _onRx64IoSampleResponse.set(func, data); }
    void onModemStatusResponse(void (*func)(ModemStatusResponse&, uintptr_t), uintptr_t data = 0) { _onModemStatusResponse.set(func, data); }
    void onAtCommandResponse(void (*func)(AtCommandResponse&, uintptr_t), uintptr_t data = 0) { _onAtCommandResponse.set(func, data); }
    void onRemoteAtCommandResponse(void (*func)(RemoteAtCommandResponse&, uintptr_t), uintptr_t data = 0) { _onRemoteAtCommandResponse.set(func, data); }

    ###
    # Regularly call this method, which ensures that the serial
    # buffer is processed and the appropriate callbacks are called.
    ###
    void loop();

    ###
    # Wait for a API response of the given type, optionally
    # filtered by the given match function.
    #
    # If a match function is given it is called for every response
    # of the right type received, passing the response and the data
    # parameter passed to this method. If the function returns true
    # (or if no function was passed), waiting stops and this method
    # returns 0. If the function returns false, waiting
    # continues. After the given timeout passes, this method
    # returns XBEE_WAIT_TIMEOUT.
    #
    # If a valid frameId is passed (e.g. 0-255 inclusive) and a
    # status API response frame is received while waiting, that has
    # a *non-zero* status, waiting stops and that status is
    # received. This is intended for when a TX packet was sent and
    # you are waiting for an RX reply, which will most likely never
    # arrive when TX failed. However, since the status reply is not
    # guaranteed to arrive before the RX reply (a remote module can
    # send a reply before the ACK), first calling waitForStatus()
    # and then waitFor() can sometimes miss the reply RX packet.
    #
    # Note that when the intended response is received *before* the
    # status reply, the latter will not be processed by this
    # method and will be subsequently processed by e.g. loop()
    # normally.
    #
    # While waiting, any other responses received are passed to the
    # relevant callbacks, just as if calling loop() continuously
    # (except for the response sought, that one is only passed to
    # the OnResponse handler and no others).
    #
    # After this method returns, the response itself can still be
    # retrieved using getResponse() as normal.
    ###
    template <typename Response>
    uint8_t waitFor(Response& response, uint16_t timeout, bool (*func)(Response&, uintptr_t) = NULL, uintptr_t data = 0, int16_t frameId = -1) {
        return waitForInternal(Response::API_ID, &response, timeout, (void*)func, data, frameId);
    }

    ###
    # Sends a XBeeRequest (TX packet) out the serial port, and wait
    # for a status response API frame (up until the given timeout).
    # Essentially this just calls send() and waitForStatus().
    # See waitForStatus for the meaning of the return value and
    # more details.
    ###
    uint8_t sendAndWait(XBeeRequest &request, uint16_t timeout) {
        send(request);
        return waitForStatus(request.getFrameId(), timeout);
    }

    ###
    # Wait for a status API response with the given frameId and
    # return the status from the packet (for ZB_TX_STATUS_RESPONSE,
    # this returns just the delivery status, not the routing
    # status). If the timeout is reached before reading the
    # response, XBEE_WAIT_TIMEOUT is returned instead.
    #
    # While waiting, any other responses received are passed to the
    # relevant callbacks, just as if calling loop() continuously
    # (except for the status response sought, that one is only
    # passed to the OnResponse handler and no others).
    #
    # After this method returns, the response itself can still be
    # retrieved using getResponse() as normal.
    ###
    uint8_t waitForStatus(uint8_t frameId, uint16_t timeout);
private:
    ###
    # Internal version of waitFor that does not need to be
    # templated (to prevent duplication the implementation for
    # every response type you might want to wait for). Instead of
    # using templates, this accepts the apiId to wait for and will
    # cast the given response object and the argument to the given
    # function to the corresponding type. This means that the
    # void* given must match the api id!
    ###
    uint8_t waitForInternal(uint8_t apiId, void *response, uint16_t timeout, void *func, uintptr_t data, int16_t frameId);

    ###
    # Helper that checks if the current response is a status
    # response with the given frame id. If so, returns the status
    # byte from the response, otherwise returns 0xff.
    ###
    uint8_t matchStatus(uint8_t frameId);

    ###
    # Top half of a typical loop(). Calls readPacket(), calls
    # onPacketError on error, calls onResponse when a response is
    # available. Returns in the true in the latter case, after
    # which a caller should typically call loopBottom().
    ###
    bool loopTop();

    ###
    # Bottom half of a typical loop. Call only when a valid
    # response was read, will call all response-specific callbacks.
    ###
    void loopBottom();

    template <typename Arg> struct Callback {
        void (*func)(Arg, uintptr_t);
        uintptr_t data;
        void set(void (*func)(Arg, uintptr_t), uintptr_t data) {
            this->func = func;
            this->data = data;
        }
        bool call(Arg arg) {
            if (this->func) {
                this->func(arg, this->data);
                return true;
            }
            return false;
        }
    };

    Callback<uint8_t> _onPacketError;
    Callback<XBeeResponse&> _onResponse;
    Callback<XBeeResponse&> _onOtherResponse;
    Callback<ZBTxStatusResponse&> _onZBTxStatusResponse;
    Callback<ZBRxResponse&> _onZBRxResponse;
    Callback<ZBExplicitRxResponse&> _onZBExplicitRxResponse;
    Callback<ZBRxIoSampleResponse&> _onZBRxIoSampleResponse;
    Callback<TxStatusResponse&> _onTxStatusResponse;
    Callback<Rx16Response&> _onRx16Response;
    Callback<Rx64Response&> _onRx64Response;
    Callback<Rx16IoSampleResponse&> _onRx16IoSampleResponse;
    Callback<Rx64IoSampleResponse&> _onRx64IoSampleResponse;
    Callback<ModemStatusResponse&> _onModemStatusResponse;
    Callback<AtCommandResponse&> _onAtCommandResponse;
    Callback<RemoteAtCommandResponse&> _onRemoteAtCommandResponse;
};

###
# All TX packets that support payloads extend this class
###
class PayloadRequest : public XBeeRequest {
public:
    PayloadRequest(uint8_t apiId, uint8_t frameId, uint8_t *payload, uint8_t payloadLength);
    ###
    # Returns the payload of the packet, if not null
    ###
    uint8_t* getPayload();
    ###
    # Sets the payload array
    ###
    void setPayload(uint8_t* payloadPtr);

    /*
    # Set the payload and its length in one call.
    ###
    void setPayload(uint8_t* payloadPtr, uint8_t payloadLength) {
        setPayload(payloadPtr);
        setPayloadLength(payloadLength);
    }

    ###
    # Returns the length of the payload array, as specified by the user.
    ###
    uint8_t getPayloadLength();
    ###
    # Sets the length of the payload to include in the request.  For example if the payload array
    # is 50 bytes and you only want the first 10 to be included in the packet, set the length to 10.
    # Length must be <= to the array length.
    ###
    void setPayloadLength(uint8_t payloadLength);
private:
    uint8_t* _payloadPtr;
    uint8_t _payloadLength;
};

#ifdef SERIES_1

###
# Represents a Series 1 TX packet that corresponds to Api Id: TX_16_REQUEST
# <p/>
# Be careful not to send a data array larger than the max packet size of your radio.
# This class does not perform any validation of packet size and there will be no indication
# if the packet is too large, other than you will not get a TX Status response.
# The datasheet says 100 bytes is the maximum, although that could change in future firmware.
###
class Tx16Request : public PayloadRequest {
public:
    Tx16Request(uint16_t addr16, uint8_t option, uint8_t *payload, uint8_t payloadLength, uint8_t frameId);
    ###
    # Creates a Unicast Tx16Request with the ACK option and DEFAULT_FRAME_ID
    ###
    Tx16Request(uint16_t addr16, uint8_t *payload, uint8_t payloadLength);
    ###
    # Creates a default instance of this class.  At a minimum you must specify
    # a payload, payload length and a destination address before sending this request.
    ###
    Tx16Request();
    uint16_t getAddress16();
    void setAddress16(uint16_t addr16);
    uint8_t getOption();
    void setOption(uint8_t option);
    uint8_t getFrameData(uint8_t pos);
    uint8_t getFrameDataLength();
protected:
private:
    uint16_t _addr16;
    uint8_t _option;
};

###
# Represents a Series 1 TX packet that corresponds to Api Id: TX_64_REQUEST
#
# Be careful not to send a data array larger than the max packet size of your radio.
# This class does not perform any validation of packet size and there will be no indication
# if the packet is too large, other than you will not get a TX Status response.
# The datasheet says 100 bytes is the maximum, although that could change in future firmware.
###
class Tx64Request : public PayloadRequest {
public:
    Tx64Request(XBeeAddress64 &addr64, uint8_t option, uint8_t *payload, uint8_t payloadLength, uint8_t frameId);
    ###
    # Creates a unicast Tx64Request with the ACK option and DEFAULT_FRAME_ID
    ###
    Tx64Request(XBeeAddress64 &addr64, uint8_t *payload, uint8_t payloadLength);
    ###
    # Creates a default instance of this class.  At a minimum you must specify
    # a payload, payload length and a destination address before sending this request.
    ###
    Tx64Request();
    XBeeAddress64& getAddress64();
    void setAddress64(XBeeAddress64& addr64);
    // TODO move option to superclass
    uint8_t getOption();
    void setOption(uint8_t option);
    uint8_t getFrameData(uint8_t pos);
    uint8_t getFrameDataLength();
private:
    XBeeAddress64 _addr64;
    uint8_t _option;
};

#endif


#ifdef SERIES_2

###
# Represents a Series 2 TX packet that corresponds to Api Id: ZB_TX_REQUEST
#
# Be careful not to send a data array larger than the max packet size of your radio.
# This class does not perform any validation of packet size and there will be no indication
# if the packet is too large, other than you will not get a TX Status response.
# The datasheet says 72 bytes is the maximum for ZNet firmware and ZB Pro firmware provides
# the ATNP command to get the max supported payload size.  This command is useful since the
# maximum payload size varies according to certain settings, such as encryption.
# ZB Pro firmware provides a PAYLOAD_TOO_LARGE that is returned if payload size
# exceeds the maximum.
###
class ZBTxRequest : public PayloadRequest {
public:
    ###
    # Creates a unicast ZBTxRequest with the ACK option and DEFAULT_FRAME_ID
    ###
    ZBTxRequest(const XBeeAddress64 &addr64, uint8_t *payload, uint8_t payloadLength);
    ZBTxRequest(const XBeeAddress64 &addr64, uint16_t addr16, uint8_t broadcastRadius, uint8_t option, uint8_t *payload, uint8_t payloadLength, uint8_t frameId);
    ###
    # Creates a default instance of this class.  At a minimum you must specify
    # a payload, payload length and a 64-bit destination address before sending
    # this request.
    ###
    ZBTxRequest();
    XBeeAddress64& getAddress64();
    uint16_t getAddress16();
    uint8_t getBroadcastRadius();
    uint8_t getOption();
    void setAddress64(const XBeeAddress64& addr64);
    void setAddress16(uint16_t addr16);
    void setBroadcastRadius(uint8_t broadcastRadius);
    void setOption(uint8_t option);
protected:
    // declare virtual functions
    uint8_t getFrameData(uint8_t pos);
    uint8_t getFrameDataLength();
    XBeeAddress64 _addr64;
    uint16_t _addr16;
    uint8_t _broadcastRadius;
    uint8_t _option;
};

###
# Represents a Series 2 TX packet that corresponds to Api Id: ZB_EXPLICIT_TX_REQUEST
#
# See the warning about maximum packet size for ZBTxRequest above,
# which probably also applies here as well.
#
# Note that to distinguish reply packets from non-XBee devices, set
# AO=1 to enable reception of ZBExplicitRxResponse packets.
###
class ZBExplicitTxRequest : public ZBTxRequest {
public:
    ###
    # Creates a unicast ZBExplicitTxRequest with the ACK option and
    # DEFAULT_FRAME_ID.
    #
    # It uses the Maxstream profile (0xc105), both endpoints 232
    # and cluster 0x0011, resulting in the same packet as sent by a
    # normal ZBTxRequest.
    ###
    ZBExplicitTxRequest(XBeeAddress64 &addr64, uint8_t *payload, uint8_t payloadLength);
    ###
    # Create a ZBExplicitTxRequest, specifying all fields.
    ###
    ZBExplicitTxRequest(XBeeAddress64 &addr64, uint16_t addr16, uint8_t broadcastRadius, uint8_t option, uint8_t *payload, uint8_t payloadLength, uint8_t frameId, uint8_t srcEndpoint, uint8_t dstEndpoint, uint16_t clusterId, uint16_t profileId);
    ###
    # Creates a default instance of this class.  At a minimum you
    # must specify a payload, payload length and a destination
    # address before sending this request.
    #
    # Furthermore, it uses the Maxstream profile (0xc105), both
    # endpoints 232 and cluster 0x0011, resulting in the same
    # packet as sent by a normal ZBExplicitTxRequest.
    ###
    ZBExplicitTxRequest();
    uint8_t getSrcEndpoint();
    uint8_t getDstEndpoint();
    uint16_t getClusterId();
    uint16_t getProfileId();
    void setSrcEndpoint(uint8_t endpoint);
    void setDstEndpoint(uint8_t endpoint);
    void setClusterId(uint16_t clusterId);
    void setProfileId(uint16_t profileId);
protected:
    // declare virtual functions
    uint8_t getFrameData(uint8_t pos);
    uint8_t getFrameDataLength();
private:
    uint8_t _srcEndpoint;
    uint8_t _dstEndpoint;
    uint16_t _profileId;
    uint16_t _clusterId;
};

#endif

###
# Represents an AT Command TX packet
# The command is used to configure the serially connected XBee radio
###
class AtCommandRequest : public XBeeRequest {
public:
    AtCommandRequest();
    AtCommandRequest(uint8_t *command);
    AtCommandRequest(uint8_t *command, uint8_t *commandValue, uint8_t commandValueLength);
    uint8_t getFrameData(uint8_t pos);
    uint8_t getFrameDataLength();
    uint8_t* getCommand();
    void setCommand(uint8_t* command);
    uint8_t* getCommandValue();
    void setCommandValue(uint8_t* command);
    uint8_t getCommandValueLength();
    void setCommandValueLength(uint8_t length);
    ###
    # Clears the optional commandValue and commandValueLength so that a query may be sent
    ###
    void clearCommandValue();
    //void reset();
private:
    uint8_t *_command;
    uint8_t *_commandValue;
    uint8_t _commandValueLength;
};

###
# Represents an Remote AT Command TX packet
# The command is used to configure a remote XBee radio
###
class RemoteAtCommandRequest : public AtCommandRequest {
public:
    RemoteAtCommandRequest();
    ###
    # Creates a RemoteAtCommandRequest with 16-bit address to set a command.
    # 64-bit address defaults to broadcast and applyChanges is true.
    ###
    RemoteAtCommandRequest(uint16_t remoteAddress16, uint8_t *command, uint8_t *commandValue, uint8_t commandValueLength);
    ###
    # Creates a RemoteAtCommandRequest with 16-bit address to query a command.
    # 64-bit address defaults to broadcast and applyChanges is true.
    ###
    RemoteAtCommandRequest(uint16_t remoteAddress16, uint8_t *command);
    ###
    # Creates a RemoteAtCommandRequest with 64-bit address to set a command.
    # 16-bit address defaults to broadcast and applyChanges is true.
    ###
    RemoteAtCommandRequest(XBeeAddress64 &remoteAddress64, uint8_t *command, uint8_t *commandValue, uint8_t commandValueLength);
    ###
    # Creates a RemoteAtCommandRequest with 16-bit address to query a command.
    # 16-bit address defaults to broadcast and applyChanges is true.
    ###
    RemoteAtCommandRequest(XBeeAddress64 &remoteAddress64, uint8_t *command);
    uint16_t getRemoteAddress16();
    void setRemoteAddress16(uint16_t remoteAddress16);
    XBeeAddress64& getRemoteAddress64();
    void setRemoteAddress64(XBeeAddress64 &remoteAddress64);
    bool getApplyChanges();
    void setApplyChanges(bool applyChanges);
    uint8_t getFrameData(uint8_t pos);
    uint8_t getFrameDataLength();
    static XBeeAddress64 broadcastAddress64;
//	static uint16_t broadcast16Address;
private:
    XBeeAddress64 _remoteAddress64;
    uint16_t _remoteAddress16;
    bool _applyChanges;
};



#endif //XBee_h

