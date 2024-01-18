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

RoleGQLModel = Annotated["RoleGQLModel", strawberry.lazy(".roleGQLModel")]

@strawberry.federation.type(
    keys=["id"], description="""Entity representing a role type (like Dean)"""
)
class RoleTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).roletypes

    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    rbacobject = resolve_rbacobject

    @strawberry.field(
        description="""List of roles with this type""",
        permission_classes=[OnlyForAuthentized(isList=True)])
    async def roles(self, info: strawberry.types.Info) -> List["RoleGQLModel"]:
        # result = await resolveRoleForRoleType(session,  self.id)
        loader = getLoadersFromInfo(info).roles
        result = await loader.filter_by(roletype_id=self.id)
        return result

#####################################################################
#
# Special fields for query
#
#####################################################################
from .utils import createInputs
from dataclasses import dataclass

@createInputs
@dataclass
class RoleTypeWhereFilter:
    id: uuid.UUID
    name: str
    from .roleGQLModel import RoleTypeWhereFilter
    roles: RoleTypeWhereFilter

@strawberryA.field(description="""Returns a list of role types""", permission_classes=[OnlyForAuthentized()])
async def role_type_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[RoleTypeWhereFilter] = None
) -> List[RoleTypeGQLModel]:
    loader = getLoadersFromInfo(info).roletype
    wf = None if where is None else strawberry.asdict(where)
    #result = await resolveProjectAll(session, skip, limit)
    result = await loader.page(skip, limit, where = wf)
    return result

role_type_by_id = createRootResolver_by_id(RoleTypeGQLModel, description="Returns role type by its id")

    
#####################################################################
#
# Mutation section
#
#####################################################################
#_______________________________INPUT_________________________________________
@strawberry.input(description="""Input model for updating a role type""")
class RoleTypeUpdateGQLModel:
    id: uuid.UUID
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None
    changed_by: uuid.UUID

@strawberry.input(description="""Input model for inserting a new role type""")
class RoleTypeInsertGQLModel:
    category_id: uuid.UUID = None
    id: Optional[uuid.UUID] = None
    name: str = None
    name_en: str = None
    createdby: strawberry.Private[uuid.UUID] = None 
    rbacobject: strawberry.Private[uuid.UUID] = None 

@strawberry.input(description="Input structure - D operation")
class RoleTypeDeleteGQLModel:
    id: uuid.UUID = strawberry.field

#_______________________________RESULT_________________________________________
@strawberry.type(description="""Result model for role type operations""")
class RoleTypeResultGQLModel:
    id: uuid.UUID = None
    msg: str = None

    @strawberry.field(description="""Result of role type operation""")
    async def role_type(self, info: strawberry.types.Info) -> Union[RoleTypeGQLModel, None]:
        result = await RoleTypeGQLModel.resolve_reference(info, self.id)
        return result
    
#_______________________________CRUD OPERACE_________________________________________
@strawberryA.mutation(description="Update the roletype record.", permission_classes=[OnlyForAuthentized()])
async def role_type_update(self, info: strawberryA.types.Info, roletype: RoleTypeUpdateGQLModel) -> RoleTypeResultGQLModel:
    user = getUserFromInfo(info)
    roletype.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).roletypes
    row = await loader.update(roletype)
    result = RoleTypeResultGQLModel()
    result.msg = "ok"
    result.id = roletype.id
    result.msg = "ok" if (row is not None) else "fail"
    # if row is None:
    #     result.msg = "fail"  
    return result
    

@strawberryA.mutation(description="Adds a new roletype record.", permission_classes=[OnlyForAuthentized()])
async def role_type_insert(self, info: strawberryA.types.Info, roletype: RoleTypeInsertGQLModel) -> RoleTypeResultGQLModel:
    user = getUserFromInfo(info)
    print(user)
    roletype.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).roletypes
    row = await loader.insert(roletype)
    result = RoleTypeResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberry.mutation(description="""Deletes a roletype""")
async def role_type_delete(self, info: strawberry.types.Info, roletype: RoleTypeDeleteGQLModel) -> RoleTypeResultGQLModel:
    loader = getLoadersFromInfo(info).roletypes

    # Perform roletype deletion operation
    deleted_row = await loader.delete(roletype.id)

    result = RoleTypeResultGQLModel()
    result.id = roletype.id

    if deleted_row is None:
        result.msg = "fail"
    else:
        result.msg = "ok"

    return result