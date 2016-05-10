# coding=utf-8
# Author: rsmith
# Copyright ©2016 iProspect, All Rights Reserved

import requests
from datetime import datetime
from xbee.config import WEB_SERVICE_PORT

data = {
    'addr': '000000000000FFFF',
    'msg': datetime.now().strftime('DATETIME %Y-%m-%d %H:%M:%S')
}

url = 'http://localhost:%d/send' % WEB_SERVICE_PORT

requests.post(url, data)
