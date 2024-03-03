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
    name = Column(String, comment="Name of the grouptype")
    name_en = Column(String, comment="English name of the grouptype")
    valid = Column(Boolean, default=True, comment="Indicates whether this entity is valid or invalid")
    groups = relationship("GroupModel", back_populates="grouptype")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp when the grouptype was created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp of the last change to the grouptype")
    createdby = UUIDFKey(nullable=True, comment="User who created this grouptype")#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True, comment="User who edited this grouptype")#Column(ForeignKey("users.id"), index=True, nullable=True)

