import datetime
import strawberry
from typing import List, Optional, Union, Annotated
import GraphTypeDefinitions
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

RoleGQLModel = Annotated["RoleGQLModel", strawberry.lazy(".roleGQLModel")]

@strawberry.federation.type(
    keys=["id"], description="""Entity representing a role type (like Dean)"""
)
class RoleTypeGQLModel(BaseGQLModel):
    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    
    @classmethod
    def getLoader(cls, info):
        return getLoader(info).roletypes

    @strawberry.field(description="""List of roles with this type""")
    async def roles(self, info: strawberry.types.Info) -> List["RoleGQLModel"]:
        # result = await resolveRoleForRoleType(session,  self.id)
        loader = getLoader(info).roles
        result = await loader.filter_by(roletype_id=self.id)
        return result

#####################################################################
#
# Special fields for query
#
#####################################################################
@strawberry.field(description="""Finds a role type by its id""")
async def role_type_by_id(
    self, info: strawberry.types.Info, id: uuid.UUID
) -> Union[RoleTypeGQLModel, None]:
    result = await RoleTypeGQLModel.resolve_reference(info, id)
    return result

@strawberry.field(description="""Finds all roles types paged""")
async def role_type_page(
    self, info: strawberry.types.Info, skip: int = 0, limit: int = 10
) -> List[RoleTypeGQLModel]:
    # result = await resolveRoleTypeAll(session,  skip, limit)
    loader = getLoader(info).roletypes
    result = await loader.page(skip, limit)
    return result

from .GraphResolvers import asPage

@strawberry.field()
@asPage
async def role_type_page(
    self, info: strawberry.types.Info, skip: int = 0, limit: int = 10
    ) -> List[RoleTypeGQLModel]:
    loader = getLoader(info).roletypes
    return loader

#####################################################################
#
# Mutation section
#
#####################################################################
import datetime
@strawberry.input(description="""Input model for updating a role type""")
class RoleTypeUpdateGQLModel:
    id: uuid.UUID
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None

@strawberry.input(description="""Input model for inserting a new role type""")
class RoleTypeInsertGQLModel:
    category_id: uuid.UUID = None
    id: Optional[uuid.UUID] = None
    name: Optional[str] = None
    name_en: Optional[str] = None

@strawberry.input(description="""Input model for deleting a role type""")
class RoleTypeDeleteGQLModel:
    id: uuid.UUID

@strawberry.type(description="""Result model for role type operations""")
class RoleTypeResultGQLModel:
    id: uuid.UUID = None
    msg: str = None

    @strawberry.field(description="""Result of role type operation""")
    async def role_type(self, info: strawberry.types.Info) -> Union[RoleTypeGQLModel, None]:
        result = await RoleTypeGQLModel.resolve_reference(info, self.id)
        return result


@strawberry.mutation(description="""Updates an existing roleType record""")
async def role_type_update(self, 
    info: strawberry.types.Info, 
    role_type: RoleTypeUpdateGQLModel

) -> RoleTypeResultGQLModel:
    print("role_type_update", role_type, flush=True)
    loader = getLoader(info).roletypes
    row = await loader.update(role_type)
    if row is not None:
        print("role_type_update", row, row.name, row.id, flush=True)
    result = RoleTypeResultGQLModel()
    result.id = role_type.id
    result.msg = "fail" if row is None else "ok"
   
    return result

@strawberry.mutation(description="""Inserts a new roleType record""")
async def role_type_insert(self, 
    info: strawberry.types.Info, 
    role_type: RoleTypeInsertGQLModel

) -> RoleTypeResultGQLModel:
    #print("role_type_update", role_type, flush=True)    
    loader = getLoader(info).roletypes
    row = await loader.insert(role_type)
    if row is not None:
        print("role_type_update", row, row.name, row.id, flush=True)
    result = RoleTypeResultGQLModel()
    result.msg = "ok"
    result.id = row.id       
    return result    

@strawberry.mutation(description="""Deletes a role type""")
async def role_type_delete(self, info: strawberry.types.Info, role_type: RoleTypeDeleteGQLModel) -> RoleTypeResultGQLModel:
    loader = getLoader(info).roletypes
    deleted_row = await loader.delete(role_type.id)
    if deleted_row is not None:
        print("role_type_update", deleted_row, deleted_row.name, deleted_row.id, flush=True)
    result = RoleTypeResultGQLModel()
    result.msg = "ok"
    result.id = deleted_row.id       
    return result   