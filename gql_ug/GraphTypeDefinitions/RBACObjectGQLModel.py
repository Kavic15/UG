import strawberry
import uuid
import asyncio
from typing import List, Annotated, Optional
from .BaseGQLModel import BaseGQLModel
from .GraphResolvers import resolve_id
from gql_ug.GraphPermissions import OnlyForAuthentized
from gql_ug.utils.Dataloaders import getLoadersFromInfo

RoleGQLModel = Annotated["RoleGQLModel", strawberry.lazy(".roleGQLModel")]

#@strawberry.federation.type(extend=False, keys=["id"])
@strawberry.federation.type(keys=["id"])
class RBACObjectGQLModel:

    id = resolve_id
    asUser: strawberry.Private[bool] = False
    asGroup: strawberry.Private[bool] = False

    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: uuid.UUID):
        if id is None: return None
                
        if isinstance(id, str): id = uuid.UUID(id)

        loaderU = getLoadersFromInfo(info).users
        loaderG = getLoadersFromInfo(info).groups
        futures = [loaderU.load(id), loaderG.load(id)]
        rows = await asyncio.gather(*futures)

        asUser = rows[0] is not None
        asGroup = rows[1] is not None

        if asUser is None and asGroup is None: return None
        
        result = RBACObjectGQLModel(asGroup=asGroup, asUser=asUser)
        result.id = id
        return result

    @strawberry.field(
        description="Roles associated with this RBAC",
        permission_classes=[OnlyForAuthentized(isList=True)])
    async def roles(self, info: strawberry.types.Info) -> List["RoleGQLModel"]:
        from .roleGQLModel import resolve_roles_on_user, resolve_roles_on_group
        result = []
        if self.asUser:
            result = await resolve_roles_on_user(self, info, user_id=self.id)
        if self.asGroup:
            result = await resolve_roles_on_group(self, info, group_id=self.id)
        return result
    
@strawberry.field(
    description="""Finds a rbacobject by its id""",
    permission_classes=[OnlyForAuthentized()])
async def rbac_by_id(
    self, info: strawberry.types.Info, id: uuid.UUID
) -> Optional["RBACObjectGQLModel"]:
    result = await RBACObjectGQLModel.resolve_reference(info=info, id=id)
    return result
