import datetime
import strawberry
import asyncio
from typing import List, Optional, Union, Annotated
import GraphTypeDefinitions
import uuid

def getLoader(info):
    return info.context["all"]

def getUser(info):
    return info.context["user"]


MembershipGQLModel = Annotated["MembershipGQLModel", strawberry.lazy(".membershipGQLModel")]
RoleGQLModel = Annotated["RoleGQLModel", strawberry.lazy(".roleGQLModel")]
GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".groupGQLModel")]


from utils.GraphPermissions import UserGDPRPermission

@strawberry.federation.type(keys=["id"], description="""Entity representing a user""")
class UserGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: uuid.UUID):
        # userloader = info.context['users']
        loader = getLoader(info).users
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
            result.__strawberry_definition__ = cls._type_definition # some version of strawberry changed :(
        return result

    @strawberry.field(description="""Entity primary key""")
    def id(self, info: strawberry.types.Info) -> uuid.UUID:
        return self.id

    @strawberry.field(description="""User's name (like John)""")
    def name(self) -> str:
        return self.name

    @strawberry.field(description="""User's family name (like Obama)""")
    def surname(self) -> str:
        return self.surname

    @strawberry.field(description="""User's email""")
    def email(self) -> Union[str, None]:
        return self.email

    @strawberry.field(description="""User's validity (if they are member of institution)""")
    def valid(self) -> bool:
        return self.valid

    @strawberry.field(description="""Time stamp""")
    def lastchange(self) -> Union[datetime.datetime, None]:
        return self.lastchange

    @strawberry.field(description="""GDPRInfo for permision test""", permission_classes=[UserGDPRPermission])
    def GDPRInfo(self, info: strawberry.types.Info) -> Union[str, None]:
        actinguser = getUser(info)
        print(actinguser)
        return "GDPRInfo"

    @strawberry.field(description="""List of groups, where the user is member""")
    async def membership(
        self, info: strawberry.types.Info
    ) -> List["MembershipGQLModel"]:
        loader = getLoader(info).memberships
        result = await loader.filter_by(user_id=self.id)
        return list(result)

    @strawberry.field(description="""List of roles, which the user has""")
    async def roles(self, info: strawberry.types.Info) -> List["RoleGQLModel"]:
        loader = getLoader(info).roles
        result = await loader.filter_by(user_id=self.id)
        return result

    @strawberry.field(
        description="""List of groups given type, where the user is member"""
    )
    async def member_of(
        self, grouptype_id: uuid.UUID, info: strawberry.types.Info
    ) -> List["GroupGQLModel"]:
        loader = getLoader(info).memberships
        rows = await loader.filter_by(user_id=self.id)# , grouptype_id=grouptype_id)
        results = (GraphTypeDefinitions.GroupGQLModel.resolve_reference(info, row.group_id) for row in rows)
        results = await asyncio.gather(*results)
        results = filter(lambda item: item.grouptype_id == grouptype_id, results)
        return results

#####################################################################
#
# Special fields for query
#
#####################################################################

@strawberry.field(description="""Returns a list of users (paged)""")
async def user_page(
    self, info: strawberry.types.Info, skip: int = 0, limit: int = 10
) -> List[UserGQLModel]:
    loader = getLoader(info).users
    result = await loader.page(skip, limit)
    return result

@strawberry.field(description="""Finds an user by their id""")
async def user_by_id(
    self, info: strawberry.types.Info, id: uuid.UUID
) -> Union[UserGQLModel, None]:
    result = await UserGQLModel.resolve_reference(info=info, id=id)
    return result

@strawberry.field(
    description="""Finds an user by letters in name and surname, letters should be atleast three"""
)
async def user_by_letters(
    self,
    info: strawberry.types.Info,
    validity: Union[bool, None] = None,
    letters: str = "",
) -> List[UserGQLModel]:
    loader = getLoader(info).users

    if len(letters) < 3:
        return []
    stmt = loader.getSelectStatement()
    model = loader.getModel()
    stmt = stmt.where((model.name + " " + model.surname).like(f"%{letters}%"))
    if validity is not None:
        stmt = stmt.filter_by(valid=True)

    result = await loader.execute_select(stmt)
    return result

from .GraphResolvers import UserByRoleTypeAndGroupStatement

@strawberry.field(description="""Finds users who plays in a group a roletype""")
async def users_by_group_and_role_type(
    self,
    info: strawberry.types.Info,
    group_id: uuid.UUID,
    role_type_id: uuid.UUID,
) -> List[UserGQLModel]:
    # result = await resolveUserByRoleTypeAndGroup(session,  group_id, role_type_id)
    loader = getLoader(info).users
    result = await loader.execute_select(UserByRoleTypeAndGroupStatement)
    return result


#####################################################################
#
# Mutation section
#
#####################################################################
import datetime

@strawberry.input(description="""Input model for updating user information""")
class UserUpdateGQLModel:
    id: uuid.UUID
    lastchange: datetime.datetime  # razitko
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
    valid: Optional[bool] = None

@strawberry.input(description="""Input model for inserting a new user""")
class UserInsertGQLModel:
    id: Optional[uuid.UUID] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
    valid: Optional[bool] = None

@strawberry.input(description="""Input model for deleting a user""")            #NOVÉ
class UserDeleteGQLModel:
    id: uuid.UUID

@strawberry.type(description="""Result model for user operations""")
class UserResultGQLModel:
    id: uuid.UUID = None
    msg: str = None

    @strawberry.field(description="""Result of user operation""")
    async def user(self, info: strawberry.types.Info) -> Union[UserGQLModel, None]:
        result = await UserGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberry.type(description="""Result model for user deletion""")              #NOVÉ##########################################
class UserDeleteResultGQLModel:
    id: uuid.UUID = None
    msg: str = None

    @strawberry.field(description="""Result of user deletion""")
    async def user(self, info: strawberry.types.Info) -> Union[UserGQLModel, None]:
        # Assuming you have a resolve_reference function for retrieving deleted user details
        result = await UserGQLModel.resolve_reference(info, self.id)
        return result                                                           ###############################################

@strawberry.mutation(description="""Updates a user's information""") #UPDATE
async def user_update(self, info: strawberry.types.Info, user: UserUpdateGQLModel) -> UserResultGQLModel:
    #print("user_update", flush=True)
    #print(user, flush=True)
    loader = getLoader(info).users
    
    updatedrow = await loader.update(user)
    #print("user_update", updatedrow, flush=True)
    result = UserResultGQLModel()
    result.id = user.id

    if updatedrow is None:
        result.msg = "fail"
    else:
        result.msg = "ok"
    print("user_update", result.msg, flush=True)
    return result

@strawberry.mutation(description="""Inserts a new user""")  #CREATE
async def user_insert(self, info: strawberry.types.Info, user: UserInsertGQLModel) -> UserResultGQLModel:
    loader = getLoader(info).users
    
    row = await loader.insert(user)

    result = UserResultGQLModel()
    result.id = row.id
    result.msg = "ok"
    
    return result

@strawberry.mutation(description="""Deletes a user""")  #DELETE
async def user_delete(self, info: strawberry.types.Info, user: UserDeleteGQLModel) -> UserDeleteResultGQLModel:
    loader = getLoader(info).users

    # Perform user deletion operation
    deleted_row = await loader.delete(user.id)

    result = UserDeleteResultGQLModel()
    result.id = user.id

    if deleted_row is None:
        result.msg = "fail"
    else:
        result.msg = "ok"

    return result