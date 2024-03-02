import strawberry as strawberryA
import datetime
import uuid
import asyncio
from typing import List, Annotated, Optional, Union
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

MembershipGQLModel = Annotated["MembershipGQLModel", strawberry.lazy(".membershipGQLModel")]
RoleGQLModel = Annotated["RoleGQLModel", strawberry.lazy(".roleGQLModel")]
GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".groupGQLModel")]

#TODO
from gql_ug.GraphPermissions import UserGDPRPermission

@strawberry.federation.type(keys=["id"], description="""Entity representing a user""")
class UserGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).users

    id = resolve_id
    name = resolve_name
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    valid = resolve_valid
    #rbacobject = resolve_rbacobject

    @strawberry.field(
        description="""User's family name (like Obama)""",
        permission_classes=[OnlyForAuthentized()])
    def surname(self) -> Optional[str]:
        return self.surname

    @strawberry.field(
        description="""User's email""",
        permission_classes=[OnlyForAuthentized()])
    def email(self) -> Optional[str]:
        return self.email

    #TODO
    # @strawberry.field(
    #     description="""GDPRInfo for permision test""", 
    #     permission_classes=[OnlyForAuthentized(), UserGDPRPermission])
    # def GDPRInfo(self, info: strawberry.types.Info) -> Union[str, None]:
    #     user_active = getUserFromInfo(info)
    #     print(user_active)
    #     return "GDPRInfo"

    @strawberry.field(
        description="""List of users, where the user is member""",
        permission_classes=[OnlyForAuthentized(isList=True)])
    async def membership(
        self, info: strawberry.types.Info
    ) -> List["MembershipGQLModel"]:
        loader = getLoadersFromInfo(info).memberships
        result = await loader.filter_by(user_id=self.id)
        return list(result)

    @strawberry.field(
        description="""List of roles, which the user has""",
        permission_classes=[OnlyForAuthentized(isList=True)])
    async def roles(self, info: strawberry.types.Info) -> List["RoleGQLModel"]:
        loader = getLoadersFromInfo(info).roles
        result = await loader.filter_by(user_id=self.id)
        return result

    @strawberry.field(
        description="""List of users given type, where the user is member""",
        permission_classes=[OnlyForAuthentized(isList=True)])
    async def member_of(
        self, grouptype_id: uuid.UUID, info: strawberry.types.Info
    ) -> List["GroupGQLModel"]:
        loader = getLoadersFromInfo(info).memberships
        rows = await loader.filter_by(user_id=self.id)# , grouptype_id=grouptype_id)
        results = (GroupGQLModel.resolve_reference(info, row.group_id) for row in rows)
        results = await asyncio.gather(*results)
        results = filter(lambda item: item.grouptype_id == grouptype_id, results)
        return results

    RBACObjectGQLModel = Annotated["RBACObjectGQLModel", strawberryA.lazy(".RBACObjectGQLModel")]
    @strawberryA.field(
        description="""""",
        permission_classes=[OnlyForAuthentized()])
    async def rbacobject(self, info: strawberryA.types.Info) -> Optional[RBACObjectGQLModel]:
        from .RBACObjectGQLModel import RBACObjectGQLModel
        result = None if self.id is None else await RBACObjectGQLModel.resolve_reference(info, self.id)
        return result

#####################################################################
#
# Special fields for query
#
#####################################################################
from .utils import createInputs
from dataclasses import dataclass
MembershipWhereFilter = Annotated["MembershipWhereFilter", strawberry.lazy(".membershipGQLModel")]

# from .GraphResolvers import createRootResolver_by_id
# user_by_id = createRootResolver_by_id(
#     scalarType=UserGQLModel, 
#     description="Returns a list of users (paged)")

@createInputs
@dataclass
class UserWhereFilter:
    id: uuid.UUID
    name: str
    surname: str
    email: str
    fullname: str
    valid: bool
    from .membershipGQLModel import MembershipWhereFilter
    memberships: MembershipWhereFilter

@strawberry.field(description="""Returns a list of users (paged)""", permission_classes=[OnlyForAuthentized()])
async def user_page(
    self, info: strawberry.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[UserWhereFilter] = None,
    orderby: Optional[str] = None,
    desc: Optional[bool] = None
) -> List[UserGQLModel]:
    wf = None if where is None else strawberry.asdict(where)
    loader = getLoadersFromInfo(info).users
    result = await loader.page(skip, limit, where=wf, orderby=orderby, desc=desc)
    return result

@strawberry.field(
    description="""Finds user id""",
    permission_classes=[OnlyForAuthentized()])
async def user_by_id(
    self, info: strawberry.types.Info, id: uuid.UUID
) -> Union[UserGQLModel, None]:
    result = await UserGQLModel.resolve_reference(info=info, id=id)
    return result

#user_page = createRootResolver_by_page(UserGQLModel, description="Returns page of users")
#user_by_id = createRootResolver_by_id(UserGQLModel, description="Returns user by it's ID")




# @strawberry.field(
#     description="""Finds an user by letters in name and surname, letters should be atleast three"""
# )
# async def user_by_letters(
#     self,
#     info: strawberry.types.Info,
#     validity: Union[bool, None] = None,
#     letters: str = "",
# ) -> List[UserGQLModel]:
#     loader = getLoader(info).users

#     if len(letters) < 3:
#         return []
#     stmt = loader.getSelectStatement()
#     model = loader.getModel()
#     stmt = stmt.where((model.name + " " + model.surname).like(f"%{letters}%"))
#     if validity is not None:
#         stmt = stmt.filter_by(valid=True)

#     result = await loader.execute_select(stmt)
#     return result

# from .GraphResolvers import UserByRoleTypeAndGroupStatement

# @strawberry.field(description="""Finds users who plays in a group a roletype""")
# async def users_by_group_and_role_type(
#     self,
#     info: strawberry.types.Info,
#     group_id: uuid.UUID,
#     role_type_id: uuid.UUID,
# ) -> List[UserGQLModel]:
#     # result = await resolveUserByRoleTypeAndGroup(session,  group_id, role_type_id)
#     loader = getLoader(info).users
#     result = await loader.execute_select(UserByRoleTypeAndGroupStatement)
#     return result


#####################################################################
#
# Mutation section
#
#####################################################################
import datetime

#_______________________________INPUT_________________________________________
@strawberry.input(description="""Input model for updating a user""")
class UserUpdateGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the financial data")
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")

    name: Optional[str]
    surname: Optional[str] = None
    email: Optional[str] = None
    valid: Optional[bool] = None
    changedby: strawberry.Private[uuid.UUID] = None

@strawberry.input(description="""Input model for inserting a new user""")
class UserInsertGQLModel:
    name: str
    #rbacobject: uuid.UUID
    id: Optional[uuid.UUID] = None
    surname: str
    email: Optional[str] = None
    valid: Optional[bool] = None
    createdby: strawberry.Private[uuid.UUID] = None
    
    
@strawberry.input(description="""Input model for deleting a user""")
class UserDeleteGQLModel:
    id: uuid.UUID

#_______________________________RESULT_________________________________________
@strawberryA.type(description="Result of user data operation")
class UserResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the user data", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns user data", permission_classes=[OnlyForAuthentized()])
    async def user(self, info: strawberryA.types.Info) -> Union[UserGQLModel, None]:
        result = await UserGQLModel.resolve_reference(info, self.id)
        return result
    
#_______________________________CRUD OPERACE_________________________________________
@strawberryA.mutation(description="Update the user record.", permission_classes=[OnlyForAuthentized()])
async def user_update(self, info: strawberryA.types.Info, user: UserUpdateGQLModel) -> UserResultGQLModel:
    user_active = getUserFromInfo(info)
    user.changedby = uuid.UUID(user_active["id"])
    loader = getLoadersFromInfo(info).users
    row = await loader.update(user)
    result = UserResultGQLModel()
    result.msg = "ok"
    result.id = user.id
    result.msg = "ok" if (row is not None) else "fail"
    # if row is None:
    #     result.msg = "fail"  
    return result
    

@strawberryA.mutation(description="Adds a new user record.", permission_classes=[OnlyForAuthentized()])
async def user_insert(self, info: strawberryA.types.Info, user: UserInsertGQLModel) -> UserResultGQLModel:
    user_active = getUserFromInfo(info)
    print(user)
    user.createdby = uuid.UUID(user_active["id"])
    loader = getLoadersFromInfo(info).users
    row = await loader.insert(user)
    result = UserResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberryA.mutation(
    description="Deletes user.",
        permission_classes=[OnlyForAuthentized()])
async def user_delete(self, info: strawberryA.types.Info, id: uuid.UUID) -> UserResultGQLModel:
    loader = getLoadersFromInfo(info).users
    row = await loader.delete(id=id)
    result = UserResultGQLModel(id=id, msg="ok")
    result.msg = "fail" if row is None else "ok"
    return result
