import strawberry as strawberryA
import datetime
import uuid
from typing import List, Annotated, Optional, Union
from .BaseGQLModel import BaseGQLModel

import strawberry
from gql_ug.utils.Dataloaders import getLoadersFromInfo, getUserFromInfo

# from gql_projects.GraphResolvers import (
#     resolveFinanceTypeById,
#     resolveProjectById,
#     resolveFinanceAll
# )

from gql_ug.GraphPermissions import RoleBasedPermission, OnlyForAuthentized

from gql_ug.GraphTypeDefinitions.GraphResolvers import (
    resolve_id,
    resolve_name,
    resolve_name_en,
    resolve_group,
    resolve_group_id,
    resolve_user,
    resolve_user_id,
    resolve_roletype,
    resolve_roletype_id,
    resolve_accesslevel,
    resolve_created,
    resolve_lastchange,
    resolve_startdate,
    resolve_enddate,
    resolve_createdby,
    resolve_changedby,
    resolve_valid,
    createRootResolver_by_id,
    createRootResolver_by_page,
    resolve_rbacobject
)

GroupTypeGQLModel = Annotated["GroupTypeGQLModel", strawberry.lazy(".groupTypeGQLModel")]
UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".userGQLModel")]

@strawberry.federation.type(keys=["id"], description="""Entity representing a relation between an user and a membership""",)
class MembershipGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).memberships

    id = resolve_id
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    user = resolve_user
    membership = resolve_group
    valid = resolve_valid
    startdate = resolve_startdate
    enddate = resolve_enddate
    rbacobject = resolve_rbacobject

#####################################################################
#
# Special fields for query
#
#####################################################################
from .utils import createInputs
from dataclasses import dataclass
GroupWhereFilter = Annotated["GroupWhereFilter", strawberry.lazy(".groupGQLModel")]
UserWhereFilter = Annotated["UserWhereFilter", strawberry.lazy(".userGQLModel")]
@createInputs
@dataclass
class MembershipWhereFilter:
    name: str
    type_id: uuid.UUID
    value: str

@strawberryA.field(description="""Returns a list of memberships""", permission_classes=[OnlyForAuthentized()])
async def membership_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[MembershipWhereFilter] = None
) -> List[MembershipGQLModel]:
    # async with withInfo(info) as session:
    #     result = await resolveFinanceTypeAll(session, skip, limit)
    #     return result
    loader = getLoadersFromInfo(info).memberships
    wf = None if where is None else strawberry.asdict(where)
    result = await loader.page(skip, limit, where = wf)
    return result

membership_by_id = createRootResolver_by_id(MembershipGQLModel, description="Returns membership by its id")

#####################################################################
#
# Mutation section
#
#####################################################################
import datetime

#_______________________________INPUT_________________________________________
@strawberry.input(description="""Input model for updating a membership""")
class MembershipUpdateGQLModel:
    id: uuid.UUID
    lastchange: datetime.datetime   
    valid: Optional[bool] = None
    startdate: Optional[datetime.datetime] = None
    enddate: Optional[datetime.datetime] = None
    changedby: strawberry.Private[uuid.UUID] = None

@strawberry.input(description="""Input model for inserting a new membership""")
class MembershipInsertGQLModel:
    user_id: uuid.UUID
    group_id: uuid.UUID
    id: Optional[uuid.UUID] = None
    valid: Optional[bool] = True
    startdate: Optional[datetime.datetime] = None
    enddate: Optional[datetime.datetime] = None
    createdby: strawberry.Private[uuid.UUID] = None

@strawberry.input(description="""Input model for deleting a membership""")
class MembershipDeleteGQLModel:
    id: uuid.UUID

#_______________________________RESULT_________________________________________
@strawberryA.type(description="Result of membership data operation")
class MembershipResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the membership data", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns membership data", permission_classes=[OnlyForAuthentized()])
    async def membership(self, info: strawberryA.types.Info) -> Union[MembershipGQLModel, None]:
        result = await MembershipGQLModel.resolve_reference(info, self.id)
        return result
    
#_______________________________CRUD OPERACE_________________________________________
@strawberry.mutation(description="""Update the membership, cannot update""", permission_classes=[OnlyForAuthentized()])
async def membership_update(self, info: strawberryA.types.Info, membership: MembershipUpdateGQLModel) -> MembershipResultGQLModel:
    user = getUserFromInfo(info)
    membership.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).memberships
    row = await loader.update(membership)
    result = MembershipResultGQLModel()
    result.msg = "ok"
    result.id = membership.id
    result.msg = "ok" if (row is not None) else "fail"
    # if row is None:
    #     result.msg = "fail"  
    return result

@strawberryA.mutation(description="Adds a new membership.", permission_classes=[OnlyForAuthentized()])
async def membership_insert(self, info: strawberryA.types.Info, membership: MembershipInsertGQLModel) -> MembershipResultGQLModel:
    user = getUserFromInfo(info)
    print(user)
    membership.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).memberships
    row = await loader.insert(membership)
    result = MembershipResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberry.mutation(description="""Deletes a membership""")
async def membership_delete(self, info: strawberry.types.Info, membership: MembershipDeleteGQLModel) -> MembershipResultGQLModel:
    loader = getLoadersFromInfo(info).memberships

    # Perform membership deletion operation
    deleted_row = await loader.delete(membership.id)

    result = MembershipResultGQLModel()
    result.id = membership.id

    if deleted_row is None:
        result.msg = "fail"
    else:
        result.msg = "ok"

    return result