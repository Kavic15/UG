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
        return getLoadersFromInfo(info).memberships

    id = resolve_id
    name =resolve_name
    name_en = resolve_name_en
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    
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
@strawberry.field(description="""Finds a role type by its id""")
async def role_category_by_id(
    self, info: strawberry.types.Info, id: uuid.UUID
) -> Union[RoleCategoryGQLModel, None]:
    result = await RoleCategoryGQLModel.resolve_reference(info,  id)
    return result

@strawberry.field(description="""gets role category page""")
async def role_category_page(
    self, info: strawberry.types.Info, skip: Optional[int] = 0, limit: Optional[int] = 10
) -> Union[RoleCategoryGQLModel, None]:
    loader = getLoader(info).rolecategories
    result = await loader.page(skip, limit)
    return result

#####################################################################
#
# Mutation section
#
#####################################################################
import datetime

@strawberry.input(description="""Input model for updating a role category""")
class RoleCategoryUpdateGQLModel:
    id: uuid.UUID
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None

@strawberry.input(description="""Input model for inserting a new role category""")
class RoleCategoryInsertGQLModel:
    id: Optional[uuid.UUID] = None
    name: Optional[str] = None
    name_en: Optional[str] = None

@strawberry.type(description="""Result model for role category operations""")
class RoleCategoryResultGQLModel:
    id: uuid.UUID = None
    msg: str = None

    @strawberry.field(description="""Result of role category operation""")
    async def role_category(self, info: strawberry.types.Info) -> Union[RoleCategoryGQLModel, None]:
        result = await RoleCategoryGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberry.mutation(description="""Updates a role category""")
async def role_category_update(self, 
    info: strawberry.types.Info, 
    role_category: RoleCategoryUpdateGQLModel

) -> RoleCategoryResultGQLModel:

    loader = getLoader(info).rolecategories
    row = await loader.update(role_category)

    result = RoleCategoryResultGQLModel()
    result.msg = "ok"
    result.id = role_category.id
    if row is None:
        result.msg = "fail"
    else:
        result.id = row.id

    
    return result

@strawberry.mutation(description="""Inserts a role category""")
async def role_category_insert(self, 
    info: strawberry.types.Info, 
    role_category: RoleCategoryInsertGQLModel

) -> RoleCategoryResultGQLModel:

    loader = getLoader(info).rolecategories
    row = await loader.insert(role_category)

    result = RoleCategoryResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    
    return result