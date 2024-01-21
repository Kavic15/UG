import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from .UUIDColumn import UUIDColumn, UUIDFKey
from .Base import BaseModel

class GroupModel(BaseModel):
    """Manages data related to group"""

    __tablename__ = "groups"

    id = UUIDColumn()
    name = Column(String, comment="Name of the group")
    name_en = Column(String, comment="English name of the group")

    #lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp of the last change to the group")

    startdate = Column(DateTime)
    enddate = Column(DateTime)
    valid = Column(Boolean, default=True)

    mastergroup_id = Column(ForeignKey("groups.id"), index=True)


    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp when the group was created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp of the last change to the group")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

