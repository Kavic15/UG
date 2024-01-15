from .UUIDColFile import UUIDColumn, UUIDFKey
from sqlalchemy import Column, DateTime, String, ForeignKey, Boolean
from .BaseModel import BaseModel
import sqlalchemy
from sqlalchemy.orm import relationship

class GroupModel(BaseModel):
    """Manages data related to group"""

    __tablename__ = "groups"

    id = UUIDColumn()
    name = Column(String, comment="Name of the group")
    name_en = Column(String, comment="English name of the group")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp of the last change to the group")

    startdate = Column(DateTime)
    enddate = Column(DateTime)
    valid = Column(Boolean, default=True)

    grouptype_id = Column(ForeignKey("grouptypes.id"), index=True)
    grouptype = relationship("GroupTypeModel", back_populates="groups")

    mastergroup_id = Column(ForeignKey("groups.id"), index=True)

    memberships = relationship("MembershipModel", back_populates="group")
    roles = relationship("RoleModel", back_populates="group")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

