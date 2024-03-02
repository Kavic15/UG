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

RoleTypeGQLModel = Annotated["RoleTypeGQLModel", strawberry.lazy(".roleTypeGQLModel")]

@strawberry.federation.type(keys=["id"], description="""Entity representing a role type (like Dean)""")
class RoleCategoryGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).rolecategories

    id = resolve_id
    name =resolve_name
    name_en = resolve_name_en
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    rbacobject = resolve_rbacobject
    
    @strawberry.field(description="""List of roles with this type""")
    async def role_types(self, info: strawberry.types.Info) -> List["RoleTypeGQLModel"]:
        # result = await resolveRoleForRoleType(session,  self.id)
        loader = getLoadersFromInfo(info).roletypes
        rows = await loader.filter_by(category_id=self.id)
        return rows
    
#####################################################################
#
# Special fields for query
#
#####################################################################

from dataclasses import dataclass
from .utils import createInputs
@createInputs
@dataclass
class RoleCategoryWhereFilter:
    name: str
    type_id: uuid.UUID
    value: str

@strawberryA.field(description="""Returns a list of finance categories""", permission_classes=[OnlyForAuthentized()])
async def role_category_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[RoleCategoryWhereFilter] = None
) -> List[RoleCategoryGQLModel]:
    # otazka: musi tady byt async? 
    # async with withInfo(info) as session:
    loader = getLoadersFromInfo(info).rolecategories
    wf = None if where is None else strawberry.asdict(where)
    #result = await resolveProjectAll(session, skip, limit)
    result = await loader.page(skip, limit, where = wf)
    return result

role_category_by_id = createRootResolver_by_id(RoleCategoryGQLModel, description="Returns finance category by its id")

#####################################################################
#
# Mutation section
#
#####################################################################
import datetime


#_______________________________INPUT_________________________________________
@strawberry.input(description="""Input model for updating a role category""")
class RoleCategoryUpdateGQLModel:
    id: uuid.UUID
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None
    changed_by: strawberry.Private[uuid.UUID] = None

@strawberry.input(description="""Input model for inserting a new role category""")
class RoleCategoryInsertGQLModel:
    id: Optional[uuid.UUID] = None
    name: str = None
    name_en: str = None
    createdby: strawberry.Private[uuid.UUID] = None 
    rbacobject: strawberry.Private[uuid.UUID] = None 

@strawberry.input(description="Input structure - D operation")
class RoleCategoryDeleteGQLModel:
    id: uuid.UUID = strawberry.field

#_______________________________RESULT_________________________________________
@strawberry.type(description="""Result model for role category operations""")
class RoleCategoryResultGQLModel:
    id: uuid.UUID = None
    msg: str = None

    @strawberry.field(description="""Result of role category operation""")
    async def role_category(self, info: strawberry.types.Info) -> Union[RoleCategoryGQLModel, None]:
        result = await RoleCategoryGQLModel.resolve_reference(info, self.id)
        return result
    
#_______________________________CRUD OPERACE_________________________________________
@strawberryA.mutation(description="Update the rolecategory record.", permission_classes=[OnlyForAuthentized()])
async def role_category_update(self, info: strawberryA.types.Info, rolecategory: RoleCategoryUpdateGQLModel) -> RoleCategoryResultGQLModel:
    user = getUserFromInfo(info)
    rolecategory.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).rolecategories
    row = await loader.update(rolecategory)
    result = RoleCategoryResultGQLModel()
    result.msg = "ok"
    result.id = rolecategory.id
    result.msg = "ok" if (row is not None) else "fail"
    # if row is None:
    #     result.msg = "fail"  
    return result
    

@strawberryA.mutation(description="Adds a new rolecategory record.", permission_classes=[OnlyForAuthentized()])
async def role_category_insert(self, info: strawberryA.types.Info, rolecategory: RoleCategoryInsertGQLModel) -> RoleCategoryResultGQLModel:
    user = getUserFromInfo(info)
    print(user)
    rolecategory.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).rolecategories
    row = await loader.insert(rolecategory)
    result = RoleCategoryResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result




# @strawberry.mutation(description="""Deletes a rolecategory""")
# async def role_category_delete(self, info: strawberry.types.Info, id: uuid.UUID) -> RoleCategoryResultGQLModel:
#     loader = getLoadersFromInfo(info).rolecategories

#     # Perform rolecategory deletion operation
#     deleted_row = await loader.delete(id = id)

#     result = RoleCategoryResultGQLModel()
#     result.id = id

#     if deleted_row is None:
#         result.msg = "fail"
#     else:
#         result.msg = "ok"

#     return result

@strawberryA.mutation(
    description="Deletes role category.",
        permission_classes=[OnlyForAuthentized()])
async def role_category_delete(self, info: strawberryA.types.Info, id: uuid.UUID) -> RoleCategoryResultGQLModel:
    loader = getLoadersFromInfo(info).rolecategories
    row = await loader.delete(id=id)
    result = RoleCategoryResultGQLModel(id=id, msg="ok")
    result.msg = "fail" if row is None else "ok"
    return result