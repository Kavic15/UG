import datetime
import strawberry
from typing import List, Optional, Union, Annotated
import gql_ug.GraphTypeDefinitions
import uuid
from .BaseGQLModel import BaseGQLModel
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

GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".groupGQLModel")]
UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".userGQLModel")]
RoleTypeGQLModel = Annotated["RoleTypeGQLModel", strawberry.lazy(".roleTypeGQLModel")]

@strawberry.federation.type(keys=["id"],description="""Entity representing a role of a user in a role (like user A in role B is Dean)""",)
class RoleGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).roles

    id = resolve_id
    changedby = resolve_changedby
    startdate = resolve_startdate
    enddate = resolve_enddate
    valid = resolve_valid
    createdby = resolve_createdby
    lastchange = resolve_lastchange
    created = resolve_created
    rbacobject = resolve_rbacobject
    roletype = resolve_roletype
    user = resolve_user
    group = resolve_group


    @strawberry.field(description="""Group where user has a role name""")
    async def role(self, info: strawberry.types.Info) -> GroupGQLModel:
        # result = await resolveGroupById(session,  self.group_id)
        result = await gql_ug.GraphTypeDefinitions.GroupGQLModel.resolve_reference(info, self.group_id)
        return result
    
#####################################################################
#
# Special fields for query
#
#####################################################################

from .utils import createInputs
from dataclasses import dataclass
# MembershipInputWhereFilter = Annotated["MembershipInputWhereFilter", strawberry.lazy(".membershipGQLModel")]
from .groupGQLModel import GroupWhereFilter
from .userGQLModel import UserWhereFilter
from .roleTypeGQLModel import RoleTypeWhereFilter

@createInputs
@dataclass

class RoleWhereFilter:
    name: str
    valid: bool
    startdate: datetime.datetime
    enddate: datetime.datetime
    from .groupGQLModel import GroupWhereFilter
    from .userGQLModel import UserWhereFilter
    # from .roleTypeGQLModel import RoleTypeWhereFilter
    group: GroupWhereFilter
    user: UserWhereFilter
    roletype: RoleTypeWhereFilter

@strawberry.field(
    description="Returns roles of user",
    permission_classes=[OnlyForAuthentized(isList=True)])
async def role_by_user(self, info: strawberry.types.Info, user_id: uuid.UUID) -> List["RoleGQLModel"]:
    loader = getLoadersFromInfo(info).roles
    rows = await loader.filter_by(user_id=user_id)
    return rows

@strawberry.field(description="""Returns a list of roles (paged)""", permission_classes=[OnlyForAuthentized()])
async def role_page(
    self, info: strawberry.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[GroupWhereFilter] = None,
    orderby: Optional[str] = None,
    desc: Optional[bool] = None
) -> List[GroupGQLModel]:
    wf = None if where is None else strawberry.asdict(where)
    loader = getLoadersFromInfo(info).roles
    result = await loader.page(skip, limit, where=wf, orderby=orderby, desc=desc)
    return result

role_by_id = createRootResolver_by_id(GroupGQLModel, description="Returns role by it's ID")

from gql_ug.DBDefinitions import RoleModel
from sqlalchemy import select

async def resolve_roles_on_user(self, info: strawberry.types.Info, user_id: uuid.UUID) -> List["RoleGQLModel"]:
    # ve vsech skupinach, kde je user clenem najdi vsechny role a ty vrat
    loaderm = getLoadersFromInfo(info).memberships
    rows = await loaderm.filter_by(user_id = user_id)
    groupids = [row.group_id for row in rows]
    # print("groupids", groupids)
    stmt = (
        select(RoleModel).
        where(RoleModel.group_id.in_(groupids))
    )
    loader = getLoadersFromInfo(info).roles
    rows = await loader.execute_select(stmt)
    return rows


async def resolve_roles_on_group(self, info: strawberry.types.Info, group_id: uuid.UUID) -> List["RoleGQLModel"]:
    # najdi vsechny role pro skupinu a nadrizene skupiny
    grouploader = getLoadersFromInfo(info).groups
    groupids = []
    cid = group_id
    while cid is not None:
        row = await grouploader.load(cid)
        if row is None:
            break
        groupids.append(row.id)
        cid = row.mastergroup_id
    # print("groupids", groupids)
    stmt = (
        select(RoleModel).
        where(RoleModel.group_id.in_(groupids))
    )
    roleloader = getLoadersFromInfo(info).roles
    rows = await roleloader.execute_select(stmt)
    return rows

@strawberry.field(
    description="""
    Returns all roles applicable on an user (defined by userId).
    If there is a dean, role with type named "dean" will be enlisted.
    """,
    permission_classes=[OnlyForAuthentized(isList=True)])
async def roles_on_user(self, info: strawberry.types.Info, user_id: uuid.UUID) -> List["RoleGQLModel"]:
    rows = await resolve_roles_on_user(self, info, user_id=user_id)
    return rows

@strawberry.field(
    description="""
    Returns all roles applicable on a group (defined by groupId).
    If the group is deparment which is subgroup of faculty, role with type named "dean" will be enlisted.
    """,
    permission_classes=[OnlyForAuthentized(isList=True)])
async def roles_on_group(self, info: strawberry.types.Info, group_id: uuid.UUID) -> List["RoleGQLModel"]:
    rows = await resolve_roles_on_group(self, info=info, group_id=group_id)
    return rows
#####################################################################
#
# Mutation section
#
#####################################################################
import datetime

#_______________________________INPUT_________________________________________
@strawberry.input(description="""Input model for updating a role""")
class RoleUpdateGQLModel:
    id: uuid.UUID
    lastchange: datetime.datetime
    valid: Optional[bool] = None
    name: Optional[str] = strawberry.field(description="The name of the financial data (optional)",default=None)
    roletype_id: uuid.UUID
    changedby: strawberry.Private[uuid.UUID] = None

@strawberry.input(description="""Input model for inserting a new role""")
class RoleInsertGQLModel:
    user_id: uuid.UUID
    group_id: uuid.UUID
    roletype_id: uuid.UUID
    id: Optional[uuid.UUID] = None
    valid: Optional[bool] = True
    startdate: Optional[datetime.datetime] = datetime.datetime.now()
    enddate: Optional[datetime.datetime] = None
    createdby: strawberry.Private[uuid.UUID] = None
    rbacobject: strawberry.Private[uuid.UUID] = None 
    
@strawberry.input(description="""Input model for deleting a role""")
class RoleDeleteGQLModel:
    id: uuid.UUID

#_______________________________RESULT_________________________________________
@strawberry.type(description="Result of role data operation")
class RoleResultGQLModel:
    id: uuid.UUID = strawberry.field(description="The ID of the role data", default=None)
    msg: str = strawberry.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberry.field(description="Returns role data", permission_classes=[OnlyForAuthentized()])
    async def role(self, info: strawberry.types.Info) -> Union[RoleGQLModel, None]:
        result = await RoleGQLModel.resolve_reference(info, self.id)
        return result
    
#_______________________________CRUD OPERACE_________________________________________
@strawberry.mutation(description="Update the role.", permission_classes=[OnlyForAuthentized()])
async def role_update(self, info: strawberry.types.Info, role: RoleUpdateGQLModel) -> RoleResultGQLModel:
    user = getUserFromInfo(info)
    role.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).roles
    row = await loader.update(role)
    result = RoleResultGQLModel()
    result.msg = "ok"
    result.id = role.id
    result.msg = "ok" if (row is not None) else "fail"
    # if row is None:
    #     result.msg = "fail"  
    return result
    

@strawberry.mutation(description="Adds a new role.", permission_classes=[OnlyForAuthentized()])
async def role_insert(self, info: strawberry.types.Info, role: RoleInsertGQLModel) -> RoleResultGQLModel:
    user = getUserFromInfo(info)
    print(user)
    role.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).roles
    row = await loader.insert(role)
    result = RoleResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberry.mutation(description="""Deletes a role""")
async def role_delete(self, info: strawberry.types.Info, role: RoleDeleteGQLModel) -> RoleResultGQLModel:
    loader = getLoadersFromInfo(info).roles

    # Perform role deletion operation
    deleted_row = await loader.delete(role.id)

    result = RoleResultGQLModel()
    result.id = role.id

    if deleted_row is None:
        result.msg = "fail"
    else:
        result.msg = "ok"

    return result