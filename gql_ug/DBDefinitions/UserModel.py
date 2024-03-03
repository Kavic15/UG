import sqlalchemy
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import relationship

from .UUIDColumn import UUIDColumn, UUIDFKey
from .Base import BaseModel

class UserModel(BaseModel):
    """Manages data related to user"""

    __tablename__ = "users"

    id = UUIDColumn()
    name = Column(String, comment="Name of the user")
    surname = Column(String, comment="Surname of the user")
    email = Column(String, comment="Email of the user")
    valid = Column(Boolean, default=True, comment="Decides if the user is valid")

    memberships = relationship("MembershipModel", back_populates="user", foreign_keys="MembershipModel.user_id")
    roles = relationship("RoleModel", back_populates="user", foreign_keys="RoleModel.user_id")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp when the user was created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp of the last change to the user")
    createdby = UUIDFKey(nullable=True, comment="User who created this user")#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True, comment="User who edited this user")#Column(ForeignKey("users.id"), index=True, nullable=True)


