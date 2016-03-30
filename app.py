# coding=utf-8
# Author: rsmith
# Copyright ©2016 That Ain't Working, All Rights Reserved

import logging
from flask import Flask, render_template

logger = logging.getLogger(__name__)


app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('index.html')


if __name__ == "__main__":
    app.run()
