import datetime
import strawberry
from typing import List, Optional, Union, Annotated
import GraphTypeDefinitions
import uuid
from .BaseGQLModel import BaseGQLModel, IDType
from .GraphResolvers import (
    resolve_id,
    resolve_name,
    resolve_name_en,
    resolve_changedby,
    resolve_created,
    resolve_lastchange,
    resolve_createdby
)

from utils.Dataloaders import (
    getLoadersFromInfo as getLoader,
    getUserFromInfo)

GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".groupGQLModel")]
UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".userGQLModel")]
RoleTypeGQLModel = Annotated["RoleTypeGQLModel", strawberry.lazy(".roleTypeGQLModel")]

@strawberry.federation.type(keys=["id"],description="""Entity representing a role of a user in a group (like user A in group B is Dean)""",)
class RoleGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoader(info).roles

    id = resolve_id
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby

    @strawberry.field(description="""If an user has still this role""")
    def valid(self) -> bool:
        return self.valid

    @strawberry.field(description="""When an user has got this role""")
    def startdate(self) -> Union[str, None]:
        return self.startdate

    @strawberry.field(description="""When an user has been removed from this role""")
    def enddate(self) -> Union[str, None]:
        return self.enddate

    @strawberry.field(description="""Role type (like Dean)""")
    async def roletype(self, info: strawberry.types.Info) -> RoleTypeGQLModel:
        # result = await resolveRoleTypeById(session,  self.roletype_id)
        result = await GraphTypeDefinitions.RoleTypeGQLModel.resolve_reference(info, self.roletype_id)
        return result

    @strawberry.field(description="""User having this role. Must be member of group?""")
    async def user(self, info: strawberry.types.Info) -> UserGQLModel:
        # result = await resolveUserById(session,  self.user_id)
        result = await GraphTypeDefinitions.UserGQLModel.resolve_reference(info, self.user_id)
        return result

    @strawberry.field(description="""Group where user has a role name""")
    async def group(self, info: strawberry.types.Info) -> GroupGQLModel:
        # result = await resolveGroupById(session,  self.group_id)
        result = await GraphTypeDefinitions.GroupGQLModel.resolve_reference(info, self.group_id)
        return result
    
#####################################################################
#
# Special fields for query
#
#####################################################################

from .GraphResolvers import asPage
@strawberry.field()
@asPage
async def role_page(self, info: strawberry.types.Info) -> List["RoleGQLModel"]:
    loader = getLoader(info).roles
    return loader

from DBDefinitions import (
    UserModel, MembershipModel, GroupModel, RoleModel
)
from sqlalchemy import select

async def resolve_roles_on_user(self, info: strawberry.types.Info, user_id: IDType) -> List["RoleGQLModel"]:
    loaderm = getLoader(info).memberships
    rows = await loaderm.filter_by(user_id = user_id)
    groupids = [row.group_id for row in rows]
    # print("groupids", groupids)
    stmt = (
        select(RoleModel).
        where(RoleModel.group_id.in_(groupids))
    )
    loader = getLoader(info).roles
    rows = await loader.execute_select(stmt)
    return rows


async def resolve_roles_on_group(self, info: strawberry.types.Info, group_id: IDType) -> List["RoleGQLModel"]:
    grouploader = getLoader(info).groups
    groupids = []
    cid = group_id
    while cid is not None:
        row = await grouploader.load(cid)
        if row is None:
            break
        groupids.append(row.id)
        cid = row.mastergroup_id
    stmt = (
        select(RoleModel).
        where(RoleModel.group_id.in_(groupids))
    )
    roleloader = getLoader(info).roles
    rows = await roleloader.execute_select(stmt)
    return rows


@strawberry.field()
async def roles_on_user(self, info: strawberry.types.Info, user_id: IDType) -> List["RoleGQLModel"]:
    rows = await resolve_roles_on_user(self, info, user_id=user_id)
    return rows

@strawberry.field()
async def roles_on_group(self, info: strawberry.types.Info, group_id: IDType) -> List["RoleGQLModel"]:
    rows = await resolve_roles_on_group(self, info=info, group_id=group_id)
    return rows

#####################################################################
#
# Mutation section
#
#####################################################################
import datetime

@strawberry.input(description="""Input model for updating a role""")
class RoleUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime
    valid: Optional[bool] = None
    startdate: Optional[datetime.datetime] = None
    enddate: Optional[datetime.datetime] = None

@strawberry.input(description="""Input model for inserting a new role""")
class RoleInsertGQLModel:
    user_id: IDType
    group_id: IDType
    roletype_id: IDType
    id: Optional[uuid.UUID] = None
    valid: Optional[bool] = True
    startdate: Optional[datetime.datetime] = datetime.datetime.now()
    enddate: Optional[datetime.datetime] = None

@strawberry.input(description="""Input model for deleting a role""")
class RoleDeleteGQLModel:
    id: IDType

@strawberry.type(description="""Result model for role operations""")
class RoleResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(description="""Result of user operation""")
    async def role(self, info: strawberry.types.Info) -> Union[RoleGQLModel, None]:
        result = await RoleGQLModel.resolve_reference(info, self.id)
        return result

@strawberry.mutation(description="""Updates a role""")
async def role_update(self, 
    info: strawberry.types.Info, 
    role: RoleUpdateGQLModel
) -> RoleResultGQLModel:
    loader = getLoader(info).roles
    updatedrow = await loader.update(role)

    result = RoleResultGQLModel()
    result.msg = "fail" if updatedrow is None else "ok"
    result.id = role.id
    
    return result

@strawberry.mutation(description="""Inserts a role""")
async def role_insert(self, 
    info: strawberry.types.Info, 
    role: RoleInsertGQLModel
) -> RoleResultGQLModel:
    
    loader = getLoader(info).roles

    result = RoleResultGQLModel()
    result.msg = "ok"
    
    updatedrow = await loader.insert(role)
    result.id = updatedrow.id
    
    return result  

@strawberry.mutation(description="""Deletes a role""")
async def role_delete(self, info: strawberry.types.Info, role: RoleDeleteGQLModel) -> RoleResultGQLModel:
    loader = getLoader(info).roles

    # Perform role deletion operation
    deleted_row = await loader.delete(role.id)

    result = RoleResultGQLModel()
    result.id = role.id

    if deleted_row is None:
        result.msg = "fail"
    else:
        result.msg = "ok"

    return result