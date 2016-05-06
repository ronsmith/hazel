# coding=utf-8
# Author: Ron Smith
# Copyright ©2016 That Ain't Working, All Rights Reserved

import logging
from flask import Flask, render_template
from models import session, Setting

logger = logging.getLogger(__name__)


app = Flask(__name__)


@app.route("/")
def hello():
    with session() as db:
        context = {s.param: s.value for s in db.query(Setting).filter(Setting.param.like('HOME_%')).all()}
        return render_template('index.html', **context)


if __name__ == "__main__":
    app.run()

