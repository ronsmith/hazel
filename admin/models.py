# coding=utf-8
# Author: rsmith
# Copyright ©2016 That Ain't Working, All Rights Reserved

import logging
from contextlib import contextmanager
from sqlalchemy import create_engine, Table, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from config import DB_URL

logger = logging.getLogger(__name__)

engine = create_engine(DB_URL) #, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


@contextmanager
def session():
    """Provide a transactional scope around a series of operations."""
    db = Session()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()


class Setting(Base):
    __tablename__ = 'Setting'

    id = Column(Integer, primary_key=True, autoincrement=True)
    param = Column(String, unique=True)
    value = Column(String)

    def __repr__(self):
        return '<Setting(id=%d, param="%s", value="%s")>' % (self.id, self.param, self.value)

    @staticmethod
    def get_value(param, default=None):

        s = Session().query(Setting).filter_by(param=param).one_or_none()
        if s and s.value:
            return s.value
        return default


user_role_assoc_table = Table(
    'UserRoleAssoc', Base.metadata,
    Column('user_id', Integer, ForeignKey('User.id')),
    Column('role_id', String, ForeignKey('Role.id')))

user_device_assoc_table = Table(
    'UserDeviceAssoc', Base.metadata,
    Column('user_id', Integer, ForeignKey('User.id')),
    Column('device_id', Integer, ForeignKey('Device.id')))


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    username = Column(String)
    password = Column(String)
    active = Column(Boolean, default=True)
    roles = relationship('Role', secondary=user_role_assoc_table)
    devices = relationship('Device', secondary=user_device_assoc_table)

    def __repr__(self):
        return '<User(id=%d, name="%s", userid="%s", active=%s)>' % (self.id, self.name, self.userid, self.active == 1)


class Role(Base):
    __tablename__ = 'Role'

    id = Column(String(2), primary_key=True)
    name = Column(String)
    users = relationship('User', secondary=user_role_assoc_table)

    def __repr__(self):
        return '<Role(id="%s", name="%s")>' % (self.id, self.name)


class DeviceType(Base):
    __tablename__ = 'DeviceType'

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String)
    driver = Column(String)
    devices = relationship('Device', back_populates='device_type')

    def __repr__(self):
        return '<DeviceType(id="%s", name="%s", driver="%s")>' % (self.id, self.name, self.driver)


class Device(Base):
    __tablename__ = 'Device'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_id = Column(Integer, ForeignKey('DeviceType.id'))
    name = Column(String)
    address = Column(Integer)
    device_type = relationship('DeviceType', back_populates='devices')
    alerts = relationship('Alert', back_populates='device')

    def __repr__(self):
        return '<Device(id=%d, type_id=%d, name="%s", address=%016X)>' % (self.id, self.type_id, self.name, self.address)


class Alert(Base):
    __tablename__ = 'Alert'

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey('Device.id'), nullable=True)
    severity = Column(Integer)
    message = Column(String)
    cleared = Column(Boolean, default=False)
    device = relationship('Device', back_populates='alerts')

    def __repr__(self):
        return '<Alert(id="%s", device_id=%d, severity=%d, cleared="%s", message="%s")>' \
               % (self.id, self.device_id, self.severity, self.cleared==1,
                  (self.message[:20] + '..') if len(self.message) > 20 else self.message)


def create_tables():
    logger.info('Creating tables for model objects.')
    Base.metadata.create_all(engine) #, checkfirst=True)


if __name__ == '__main__':
    create_tables()
