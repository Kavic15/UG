# import uuid
# from sqlalchemy import (
#     Column,
#     String
# )


# def newUuidAsString():
#     return f"{uuid.uuid1()}"


# def UUIDColumn(name=None):
#     if name is None:
#         return Column(String, primary_key=True, unique=True, default=newUuidAsString)
#     else:
#         return Column(
#             name, String, primary_key=True, unique=True, default=newUuidAsString
#         )


# def UUIDFKey(*, ForeignKey=None, nullable=False):
#     if ForeignKey is None:
#         return Column(
#             String, index=True, nullable=nullable
#         )
#     else:
#         return Column(
#             ForeignKey, index=True, nullable=nullable
#         )

from uuid import uuid4, UUID
from sqlalchemy import Column, Uuid
uuid = uuid4

def UUIDFKey(comment=None, nullable=True, **kwargs):
    return Column(Uuid, index=True, comment=comment, nullable=nullable, **kwargs)

def UUIDColumn():
    return Column(Uuid, primary_key=True, comment="primary key", default=uuid)  