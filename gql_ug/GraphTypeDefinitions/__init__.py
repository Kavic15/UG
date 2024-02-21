import typing
from typing import List, Union, Optional
import strawberry as strawberry
import uuid
import datetime
from .RBACObjectGQLModel import RBACObjectGQLModel

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
# from .GraphResolvers import resolveMembershipById

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

from .userGQLModel import UserGQLModel # jen jako demo
from .groupGQLModel import GroupGQLModel
from .groupTypeGQLModel import GroupTypeGQLModel
from .membershipGQLModel import MembershipGQLModel
from .roleGQLModel import RoleGQLModel
from .roleCategoryGQLModel import RoleCategoryGQLModel
from .roleTypeGQLModel import RoleTypeGQLModel

schema = strawberry.federation.Schema(query=Query, types=(RBACObjectGQLModel, uuid.UUID), mutation=Mutation)

# schema = strawberry.federation.Schema(
#     query=Query,
#     types=(
#         UserGQLModel,
#         GroupGQLModel,
#         GroupTypeGQLModel,
#         MembershipGQLModel,
#         RoleGQLModel,
#         RoleCategoryGQLModel,    
#         RoleTypeGQLModel,
#         RBACObjectGQLModel, uuid.UUID),
#     mutation=Mutation)
