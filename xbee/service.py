# coding=utf-8
# Author: Ron Smith
# Copyright ©2016 That Ain't Working, All Rights Reserved

import logging
from flask import Flask, render_template, request, abort
from flask.ext.autodoc import Autodoc
from xbee.transparent import XBeeTransparent, XBeeTransparentListener
from xbee.config import XBEE_PORT_CONFIG, WEB_SERVICE_PORT, BROADCAST_PORT
from xbee.broadcaster import UDPBroadcaster

logger = logging.getLogger(__name__)


app = Flask('XbeeService')
auto = Autodoc(app)

bcaster = UDPBroadcaster(BROADCAST_PORT)


def publish_incoming(line):
    bcaster.send(line)


xbee = XBeeTransparent(*XBEE_PORT_CONFIG)
xbee.listener = XBeeTransparentListener(publish_incoming)


@app.route('/')
def index():
    render_template('index.html')


@app.route('/docs')
def docs():
    """Returns documentation for the service endpoints."""
    try:
        return auto.html(title='Xbee Microservice API')
    except:
        logger.exception('Failed to render template.')


@app.route('/send', methods=['GET', 'POST'])
def send():
    try:
        addr = int(request.values['addr'], 16)
        msg = request.values['msg']
        xbee.transmit(msg, addr)
    except KeyError:
        logger.exception('Send request missing required data.')
        abort(400)
    except:
        logger.exception('Failed to send.')
        abort(500)


if __name__ == "__main__":
    app.run(host='localhost', port=WEB_SERVICE_PORT)

