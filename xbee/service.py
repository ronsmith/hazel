# coding=utf-8
# Author: Ron Smith
# Copyright ©2016 That Ain't Working, All Rights Reserved

import logging
from flask import Flask, render_template
from flask.ext.autodoc import Autodoc

logger = logging.getLogger(__name__)


app = Flask(__name__)
auto = Autodoc(app)


@app.route("/")
def index():
    render_template('index.html')


@app.route('/docs/')
def docs():
    """Returns documentation for the service endpoints."""
    try:
        return auto.html(title='Xbee Microservice API')
    except:
        logger.exception('Failed to render template.')


if __name__ == "__main__":
    app.run()

