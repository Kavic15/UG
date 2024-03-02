import datetime
import strawberry as strawberryA
from typing import List, Optional, Union, Annotated
import uuid
from .BaseGQLModel import BaseGQLModel
import strawberry
from gql_ug.utils.Dataloaders import getLoadersFromInfo, getUserFromInfo

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


#GroupTypeGQLModel = Annotated["GroupTypeGQLModel", strawberry.lazy(".groupTypeGQLModel")]
MembershipGQLModel = Annotated["MembershipGQLModel", strawberry.lazy(".membershipGQLModel")]
RoleGQLModel = Annotated["RoleGQLModel", strawberry.lazy(".roleGQLModel")]
GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".groupGQLModel")]
RBACObjectGQLModel = Annotated["RBACObjectGQLModel", strawberry.lazy(".RBACObjectGQLModel")]

@strawberry.federation.type(keys=["id"], description="""Entity representing a group type (like Faculty)""")
class GroupTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).grouptypes
        
    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    rbacobject = resolve_rbacobject
    valid = resolve_valid

    @strawberry.field(description="""List of groups which have this type""")
    async def groups(
        self, info: strawberry.types.Info
    ) -> List["GroupGQLModel"]:
        # result = await resolveGroupForGroupType(session,  self.id)
        loader = getLoadersFromInfo(info).groups
        result = await loader.filter_by(grouptype_id=self.id)
        return result

#####################################################################
#
# Special fields for query
#
#####################################################################
from .utils import createInputs
from dataclasses import dataclass
# MembershipInputWhereFilter = Annotated["MembershipInputWhereFilter", strawberry.lazy(".membershipGQLModel")]
@createInputs
@dataclass
class GroupTypeWhereFilter:
    id: uuid.UUID
    name: str
    valid: bool


@strawberry.field(description="""Returns a list of group types (paged)""", permission_classes=[OnlyForAuthentized()])
async def group_type_page(
    self, info: strawberry.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[GroupTypeWhereFilter] = None,
    orderby: Optional[str] = None,
    desc: Optional[bool] = None
) -> List[GroupGQLModel]:
    wf = None if where is None else strawberry.asdict(where)
    loader = getLoadersFromInfo(info).grouptypes
    result = await loader.page(skip, limit, where=wf, orderby=orderby, desc=desc)
    return result

group_type_by_id = createRootResolver_by_id(GroupTypeGQLModel, description="Returns group type by its id")

# @strawberry.field(description="""Finds a group type by its id""")
# async def group_type_by_id(
#     self, info: strawberry.types.Info, id: uuid.UUID
# ) -> Union[GroupTypeGQLModel, None]:
#     # result = await resolveGroupTypeById(session,  id)
#     result = await GroupTypeGQLModel.resolve_reference(info, id)
#     return result

#####################################################################
#
# Mutation section
#
#####################################################################
import datetime

#_______________________________INPUT_________________________________________
@strawberry.input(description="""Input model for updating a group type""")
class GroupTypeUpdateGQLModel:
    id: uuid.UUID
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None
    changedby: strawberry.Private[uuid.UUID] = None

@strawberry.input(description="""Input model for inserting a new group type""")
class GroupTypeInsertGQLModel:
    id: Optional[uuid.UUID] = None
    name: Optional[str] = None
    name_en: Optional[str] = None
    createdby: strawberry.Private[uuid.UUID] = None
    
@strawberry.input(description="""Input model for deleting a group type""")
class GroupTypeDeleteGQLModel:
    id: uuid.UUID

#_______________________________RESULT_________________________________________
@strawberryA.type(description="Result of group data operation")
class GroupTypeResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the group type data", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns group type data", permission_classes=[OnlyForAuthentized()])
    async def group_type(self, info: strawberryA.types.Info) -> Union[GroupTypeGQLModel, None]:
        result = await GroupTypeGQLModel.resolve_reference(info, self.id)
        return result
    
#_______________________________CRUD OPERACE_________________________________________
@strawberryA.mutation(description="Update the group type.", permission_classes=[OnlyForAuthentized()])
async def group_type_update(self, info: strawberryA.types.Info, grouptype: GroupTypeUpdateGQLModel) -> GroupTypeResultGQLModel:
    user = getUserFromInfo(info)
    grouptype.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).grouptypes
    row = await loader.update(grouptype)
    result = GroupTypeResultGQLModel()
    result.msg = "ok"
    result.id = grouptype.id
    result.msg = "ok" if (row is not None) else "fail"
    # if row is None:
    #     result.msg = "fail"
    return result
    

@strawberryA.mutation(description="Adds a new group type record.", permission_classes=[OnlyForAuthentized()])
async def group_type_insert(self, info: strawberryA.types.Info, grouptype: GroupTypeInsertGQLModel) -> GroupTypeResultGQLModel:
    user = getUserFromInfo(info)
    print(user)
    grouptype.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).grouptypes
    row = await loader.insert(grouptype)
    result = GroupTypeResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

# @strawberry.mutation(description="""Deletes a group type""")
# async def group_type_delete(self, info: strawberry.types.Info, grouptype: GroupTypeDeleteGQLModel) -> GroupTypeResultGQLModel:
#     loader = getLoadersFromInfo(info).grouptypes

#     # Perform grouptype deletion operation
#     deleted_row = await loader.delete(grouptype.id)

#     result = GroupTypeResultGQLModel()
#     result.id = grouptype.id

#     if deleted_row is None:
#         result.msg = "fail"
#     else:
#         result.msg = "ok"

#     return result

@strawberryA.mutation(
    description="Deletes group type.",
        permission_classes=[OnlyForAuthentized()])
async def group_type_delete(self, info: strawberryA.types.Info, id: uuid.UUID) -> GroupTypeResultGQLModel:
    loader = getLoadersFromInfo(info).grouptypes
    row = await loader.delete(id=id)
    result = GroupTypeResultGQLModel(id=id, msg="ok")
    result.msg = "fail" if row is None else "ok"
    return result