# coding=utf-8
# Created by Ron Smith on 5/8/2016
# Copyright ©2016 That Ain't Working, All Rights Reserved


def tobytes(v):
    if isinstance(v, (bytes, bytearray)):
        return v
    else:
        return bytes(v, 'utf8')
