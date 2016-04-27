# coding=utf-8
# Author: rsmith
# Copyright ©2016 iProspect, All Rights Reserved

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


# Create ORM through reflection
engine = create_engine('sqlite:///hazel.db') #, echo=True)
Base = automap_base(bind=engine)
Base.prepare(engine, reflect=True)
session = Session(engine)

# Create simple aliases for reflected model classes
Setting = Base.classes.Setting
User = Base.classes.User
Role = Base.classes.Role
Device = Base.classes.Device
DeviceType = Base.classes.DeviceType
Alert = Base.classes.Alert


# Define some nice repr strings for the automapped classes

def _seetting_repr(self):
    return '<Setting(id=%d, param="%s", value="%s")>' % (self.id, self.param, self.value)


def _setting_get_value(param, default=None):
    s = session.query(Setting).filter_by(param=param).one_or_none()
    if s and s.value:
        return s.value
    return default


Setting.__repr__ = _seetting_repr
Setting.get_value = staticmethod(_setting_get_value)


def _user_repr(self):
    return '<User(id=%d, name="%s", userid="%s", active=%s)>' % (self.id, self.name, self.userid, self.active==1)


User.__repr__ = _user_repr


def _role_repr(self):
    return '<Role(id="%s", name="%s")>' % (self.id, self.name)


Role.__repr__ = _role_repr


def _device_repr(self):
    return '<Device(id=%d, type_id=%d, name="%s", address=%016X)>' % (self.id, self.type_id, self.name, self.address)


Device.__repr__ = _device_repr


def _devicetype_repr(self):
    return '<DeviceType(id="%s", name="%s", driver="%s")>' % (self.id, self.name, self.driver)


DeviceType.__repr__ = _devicetype_repr


def _alert_repr(self):
    return '<Alert(id="%s", device_id=%d, severity=%d, cleared="%s", message="%s")>' \
           % (self.id, self.device_id, self.severity, self.cleared==1,
              (self.message[:20] + '..') if len(self.message) > 20 else self.message)


Alert.__repr__ = _alert_repr

