# coding=utf-8
# Author: Ron Smith
# Copyright ©2016 That Ain't Working, All Rights Reserved

import logging
from flask import Flask, render_template, request, abort, redirect
from flask.ext.autodoc import Autodoc
from xbee.transparent import XBeeTransparent, XBeeTransparentListener
from xbee.config import XBEE_SERIAL_CONFIG, WEB_SERVICE_PORT, BROADCAST_PORT
from xbee.broadcaster import UDPBroadcaster

logger = logging.getLogger(__name__)


app = Flask(__name__)
auto = Autodoc(app)

bcaster = UDPBroadcaster(BROADCAST_PORT)


def publish_incoming(line):
    bcaster.send(line)


xbee = XBeeTransparent(*XBEE_SERIAL_CONFIG)
xbee.listener = XBeeTransparentListener(publish_incoming)


@app.route('/')
def index():
    try:
        return render_template('index.html')
    except:
        logger.exception("Error rendering template: index.html")
        raise


@app.route('/docs')
def docs():
    """Returns documentation for the service endpoints."""
    try:
        return auto.html(title='Xbee Microservice API')
    except:
        logger.exception('Failed to generate documentation.')
        raise


@app.route('/send', methods=['GET', 'POST'])
@auto.doc()
def send():
    """
    Send an XBee message

    Parameters
        addr: 64-bit hex destination address, i.e. 000000000000FFFF
        msg: UTF8 message text
        interactive: [optional] if "true", this endpoint will redirect to the index page. Defaults to false.
    """
    try:
        addr = int(request.values['addr'], 16)
        msg = request.values['msg']
        interactive = request.values.get('interactive', False)
        if interactive:
            interactive = interactive.lower() == 'true'

        logger.info('Sending to %016X: %s' % (addr, msg))
        xbee.transmit(msg, addr)

        if interactive:
            return redirect('/')
        else:
            return '200 OK'
    except KeyError:
        logger.exception('Send request missing required data.')
        abort(400)
    except:
        logger.exception('Failed to send.')
        abort(500)


if __name__ == "__main__":
    app.run(host='localhost', port=WEB_SERVICE_PORT)

