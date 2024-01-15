import datetime
import strawberry
from typing import List, Optional, Union, Annotated
import uuid
from .BaseGQLModel import BaseGQLModel
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


def getLoader(info):
    return info.context["all"]

RoleTypeGQLModel = Annotated["RoleTypeGQLModel", strawberry.lazy(".roleTypeGQLModel")]

@strawberry.federation.type(keys=["id"], description="""Entity representing a role type (like Dean)""")
class RoleCategoryGQLModel(BaseGQLModel):
    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    
    @classmethod
    def getLoader(cls, info):
        return getLoader(info).rolecategories

    @strawberry.field(description="""List of roles with this type""")
    async def role_types(self, info: strawberry.types.Info) -> List["RoleTypeGQLModel"]:
        # result = await resolveRoleForRoleType(session,  self.id)
        loader = getLoader(info).roletypes
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
    result.msg = result.msg = "fail" if row is None else "ok"
    
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