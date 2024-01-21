import typing
from typing import List, Union, Optional
import strawberry as strawberryA
import uuid
import datetime

from contextlib import asynccontextmanager


@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context["asyncSessionMaker"]
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass


def getLoader(info):
    return info.context["all"]


import datetime

# @strawberryA.federation.type(
#     keys=["id"],
#     description="""Entity representing a relation between an user and a group""",
# )
# class UGInsertGQLModel:
#     @classmethod
#     async def resolve_reference(cls, info: strawberryA.types.Info):
#         result = UGInsertGQLModel()
#         return result

#     @strawberryA.field(description="""Inserts new membership""")
#     async def id(self) -> strawberryA.ID:
#         return 1

#     @strawberryA.field(description="""Inserts new membership""")
#     async def membership_insert(self, 
#         info: strawberryA.types.Info, 
#         membership: "MembershipInsertGQLModel"
#     ) -> "MembershipResultGQLModel":

#         loader = getLoader(info).memberships
#         row = await loader.insert(membership)

#         result = MembershipResultGQLModel()
#         result.msg = "ok"
#         result.id = row.id
        
#         return result
    
###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

from .query import Query
from .mutation import Mutation

from .groupGQLModel import GroupGQLModel

schema = strawberryA.federation.Schema(
    query=Query,
    types=(
        GroupGQLModel,
        uuid.UUID),
    mutation=Mutation)