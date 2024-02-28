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

class MembershipModel(BaseModel):
    """Spojuje User s Group jestlize User je clen Group
    Umoznuje udrzovat historii spojeni
    """

    __tablename__ = "memberships"

    id = UUIDColumn()
    user_id = Column(ForeignKey("users.id"), index=True)
    group_id = Column(ForeignKey("groups.id"), index=True)

    valid = Column(Boolean, default=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

    user = relationship("UserModel", back_populates="memberships")
    group = relationship("GroupModel", back_populates="memberships")
