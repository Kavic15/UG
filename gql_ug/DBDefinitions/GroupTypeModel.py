import sqlalchemy
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import relationship

from .UUIDColumn import UUIDColumn, UUIDFKey
from .Base import BaseModel


class GroupTypeModel(BaseModel):
    """Urcuje typ skupiny (fakulta, katedra, studijni skupina apod.)"""

    __tablename__ = "grouptypes"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    valid = Column(Boolean, default=True, comment="Indicates whether this entity is valid or invalid")
    groups = relationship("GroupModel", back_populates="grouptype")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

