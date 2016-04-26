# coding=utf-8
# Author: rsmith
# Copyright ©2016 iProspect, All Rights Reserved

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


# Create ORM through reflection
engine = create_engine('sqlite:///hazel.db', echo=True)
Base = automap_base(bind=engine)
Base.prepare(engine, reflect=True)


# Create simple aliases for reflected model classes
User = Base.classes.User
Role = Base.classes.Role
Device = Base.classes.Device
Type = Base.classes.Type


session = Session(engine)
