# coding=utf-8
# Author: Ron Smith
# Copyright ©2016 That Ain't Working, All Rights Reserved

import os
from logging.config import dictConfig as logger_config


XBEE_SERIAL_PORT = os.environ.get('XBEE_SERIAL_PORT', '/dev/ttyUSB0')

XBEE_SERIAL_CONFIG = (XBEE_SERIAL_PORT, 9600, 8, 'N', 1)

WEB_SERVICE_PORT = 50001

BROADCAST_PORT = 50002


logger_config({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        },
        # 'scheduler': {
        #     'handlers': ['default'],
        #     'level': 'DEBUG',
        #     'propagate': True
        # },
    }
})
