# coding=utf-8
# Author: Ron Smith
# Copyright ©2016 That Ain't Working, All Rights Reserved

import logging
from flask import Flask, render_template, request, abort
from flask.ext.autodoc import Autodoc
from xbee.transparent import XBeeTransparent, XBeeTransparentListener
from xbee.config import XBEE_PORT_CONFIG, WEB_SERVICE_CONFIG

logger = logging.getLogger(__name__)


app = Flask('XbeeService')
auto = Autodoc(app)


def publish_incoming(line):
    pass  # TODO


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
        dh = request.values['dh']
        dl = request.values['dl']
        msg = request.values['msg']
        # TODO
    except KeyError:
        logger.exception('Send request missing required data.')
        abort(400)
    except:
        logger.exception('Failed to send.')
        abort(500)


if __name__ == "__main__":
    app.run(host=WEB_SERVICE_CONFIG[0], port=WEB_SERVICE_CONFIG[1])

