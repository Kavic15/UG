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
MembershipGQLModel = Annotated["MembershipGQLModel", strawberry.lazy(".membershipGQLModel")]
RoleGQLModel = Annotated["RoleGQLModel", strawberry.lazy(".roleGQLModel")]

@strawberry.federation.type(keys=["id"], description="""Entity representing a group""")
class GroupGQLModel(BaseGQLModel):
    @classmethod

    def getLoader(cls, info):
        return getLoadersFromInfo(info).groups

    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en

    startdate = resolve_startdate
    enddate = resolve_enddate
    valid = resolve_valid

    changedby = resolve_changedby
    lastchange = resolve_lastchange
    created = resolve_created
    createdby = resolve_createdby
    
    rbacobject = resolve_rbacobject

    @strawberryA.field(description="""Type of group""", permission_classes=[OnlyForAuthentized()])
    async def grouptype(
        self, info: strawberryA.types.Info
    ) -> List["GroupTypeGQLModel"]:
        loader = getLoadersFromInfo(info).grouptypes
        result = await loader.filter_by(id = self.grouptype_id)
        return result

    @strawberry.field(description="""Directly commanded groups""", permission_classes=[OnlyForAuthentized(isList=True)])
    async def subgroups(
        self, info: strawberry.types.Info
    ) -> List["GroupGQLModel"]:
        loader = getLoadersFromInfo(info).groups
        print(self.id)
        result = await loader.filter_by(mastergroup_id=self.id)
        return result

    @strawberry.field(description="""Commanding group""", permission_classes=[OnlyForAuthentized()])
    async def mastergroup(
        self, info: strawberry.types.Info
    ) -> Optional["GroupGQLModel"]:
        result = await GroupGQLModel.resolve_reference(info, id=self.mastergroup_id)
        return result

    @strawberry.field(description="""List of users who are member of the group""", permission_classes=[OnlyForAuthentized(isList=True)])
    async def memberships(
        self, info: strawberry.types.Info
    ) -> List["MembershipGQLModel"]:

        loader = getLoadersFromInfo(info).memberships
        #print(self.id)
        result = await loader.filter_by(group_id=self.id)
        return result

    @strawberry.field(
        description="""List of roles in the group""",
        permission_classes=[OnlyForAuthentized(isList=True)])
    async def roles(self, info: strawberry.types.Info) -> List["RoleGQLModel"]:
        # result = await resolveRolesForGroup(session,  self.id)
        loader = getLoadersFromInfo(info).roles
        result = await loader.filter_by(group_id=self.id)
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
class GroupWhereFilter:
    id: uuid.UUID
    name: str
    valid: bool
    from .membershipGQLModel import MembershipWhereFilter
    memberships: MembershipWhereFilter

@strawberry.field(description="""Returns a list of groups (paged)""", permission_classes=[OnlyForAuthentized()])
async def group_page(
    self, info: strawberry.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[GroupWhereFilter] = None,
    orderby: Optional[str] = None,
    desc: Optional[bool] = None
) -> List[GroupGQLModel]:
    wf = None if where is None else strawberry.asdict(where)
    loader = getLoadersFromInfo(info).groups
    result = await loader.page(skip, limit, where=wf, orderby=orderby, desc=desc)
    return result

#group_page = createRootResolver_by_page(GroupGQLModel, description="Returns page of groups")
group_by_id = createRootResolver_by_id(GroupGQLModel, description="Returns group by it's ID")

# @strawberry.field(
#     description="""Finds a group by its id""",
#     permission_classes=[OnlyForAuthentized()])
# async def group_by_id(
#     self, info: strawberry.types.Info, id: uuid.UUID
# ) -> Union[GroupGQLModel, None]:
#     result = await GroupGQLModel.resolve_reference(info=info, id=id)
#     return result


#TODO
# @strawberry.field(
#     description="""Finds an user by letters in name and surname, letters should be atleast three""",
#     deprecation_reason='replaced by `query($letters: String!){groupPage(where: {name: {_like: $letters}}) { id name }}`',
#     permission_classes=[OnlyForAuthentized()]
# )
# async def group_by_letters(
#     self,
#     info: strawberry.types.Info,
#     validity: Union[bool, None] = None,
#     letters: str = "",
# ) -> List[GroupGQLModel]:
#     # result = await resolveGroupsByThreeLetters(session,  validity, letters)
#     loader = getLoader(info).groups

#     if len(letters) < 3:
#         return []
#     stmt = loader.getSelectStatement()
#     model = loader.getModel()
#     stmt = stmt.where(model.name.like(f"%{letters}%"))
#     if validity is not None:
#         stmt = stmt.filter_by(valid=True)

#     result = await loader.execute_select(stmt)
#     return result

# @strawberry.field(description="""Random university""")
# async def randomUniversity(
#     self, name: str, info: strawberry.types.Info
# ) -> GroupGQLModel:
#     async with withInfo(info) as session:
#         # newId = await randomDataStructure(session,  name)
#         newId = await randomDataStructure(session, name)
#         print("random university id", newId)
#         # result = await resolveGroupById(session,  newId)
#         result = await resolveGroupById(session, newId)
#         print("db response", result.name)
#         return result

#####################################################################
#
# Mutation section
#
#####################################################################
import datetime

#_______________________________INPUT_________________________________________
@strawberry.input(description="""Input model for updating a group""")
class GroupUpdateGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the financial data")
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")

    name: Optional[str] = strawberryA.field(description="The name of the financial data (optional)",default=None)
    grouptype_id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the financial data type (optional)",default=None)
    mastergroup_id: Optional[float] = strawberryA.field(description="The amount of financial data (optional)", default=None)
    valid: Optional[bool] = None
    changedby: strawberry.Private[uuid.UUID] = None

@strawberry.input(description="""Input model for inserting a new group""")
class GroupInsertGQLModel:
    name: str = strawberryA.field(description="Name of the financial data")
    grouptype_id: uuid.UUID
    id: Optional[uuid.UUID] = None
    name_en: Optional[str] = None
    mastergroup_id: Optional[uuid.UUID] = None
    valid: Optional[bool] = None
    createdby: strawberry.Private[uuid.UUID] = None
    
@strawberry.input(description="""Input model for deleting a group""")
class GroupDeleteGQLModel:
    id: uuid.UUID

#_______________________________RESULT_________________________________________
@strawberryA.type(description="Result of group data operation")
class GroupResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the group data", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns group data", permission_classes=[OnlyForAuthentized()])
    async def group(self, info: strawberryA.types.Info) -> Union[GroupGQLModel, None]:
        result = await GroupGQLModel.resolve_reference(info, self.id)
        return result
    
#_______________________________CRUD OPERACE_________________________________________
@strawberryA.mutation(description="Update the group record.", permission_classes=[OnlyForAuthentized()])
async def group_update(self, info: strawberryA.types.Info, group: GroupUpdateGQLModel) -> GroupResultGQLModel:
    user = getUserFromInfo(info)
    group.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).groups
    row = await loader.update(group)
    result = GroupResultGQLModel()
    result.msg = "ok"
    result.id = group.id
    result.msg = "ok" if (row is not None) else "fail"
    # if row is None:
    #     result.msg = "fail"  
    return result
    

@strawberryA.mutation(description="Adds a new group record.", permission_classes=[OnlyForAuthentized()])
async def group_insert(self, info: strawberryA.types.Info, group: GroupInsertGQLModel) -> GroupResultGQLModel:
    user = getUserFromInfo(info)
    print(user)
    group.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).groups
    row = await loader.insert(group)
    result = GroupResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberry.mutation(description="""Deletes a group""")
async def group_delete(self, info: strawberry.types.Info, group: GroupDeleteGQLModel) -> GroupResultGQLModel:
    loader = getLoadersFromInfo(info).groups

    # Perform group deletion operation
    deleted_row = await loader.delete(group.id)

    result = GroupResultGQLModel()
    result.id = group.id

    if deleted_row is None:
        result.msg = "fail"
    else:
        result.msg = "ok"

    return result

@strawberry.mutation(description="""Allows to assign the group to specified master group""")
async def group_update_master(self, 
    info: strawberry.types.Info, 
    master_id: uuid.UUID,
    group: GroupUpdateGQLModel) -> GroupResultGQLModel:
    user = getUserFromInfo(info)
    loader = getLoadersFromInfo(info).groups

    group.updatedby = uuid.UUID(user["id"])
    
    result = GroupResultGQLModel()
    result.id = group.id
    result.msg = "ok"

    #use asyncio.gather here
    updatedrow = await loader.load(group.id)
    if updatedrow is None:
        result.msg = "fail"
        return result

    masterrow = await loader.load(master_id)
    if masterrow is None:
        result.msg = "fail"
        return result

    updatedrow.master_id = master_id
    updatedrow = await loader.update(updatedrow)
    
    if updatedrow is None:
        result.msg = "fail"
    
    return result