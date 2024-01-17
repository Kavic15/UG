import datetime
import strawberry
from typing import List, Optional, Union, Annotated
import gql_ug.GraphTypeDefinitions
import uuid

def getLoader(info):
    return info.context["all"]

GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".groupGQLModel")]
UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".userGQLModel")]
RoleTypeGQLModel = Annotated["RoleTypeGQLModel", strawberry.lazy(".roleTypeGQLModel")]

@strawberry.federation.type(keys=["id"],description="""Entity representing a role of a user in a group (like user A in group B is Dean)""",)
class RoleGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: uuid.UUID):
        # result = await resolverRoleById(session,  id)
        loader = getLoader(info).roles
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
            result.__strawberry_definition__ = cls._type_definition # some version of strawberry changed :(
        return result

    @strawberry.field(description="""Primary key""")
    def id(self) -> uuid.UUID:
        return self.id

    @strawberry.field(description="""Time stamp""")
    def lastchange(self) -> uuid.UUID:
        return self.lastchange

    @strawberry.field(description="""If an user has still this role""")
    def valid(self) -> bool:
        return self.valid

    @strawberry.field(description="""When an user has got this role""")
    def startdate(self) -> Union[str, None]:
        return self.startdate

    @strawberry.field(description="""When an user has been removed from this role""")
    def enddate(self) -> Union[str, None]:
        return self.enddate

    @strawberry.field(description="""Role type (like Dean)""")
    async def roletype(self, info: strawberry.types.Info) -> RoleTypeGQLModel:
        # result = await resolveRoleTypeById(session,  self.roletype_id)
        result = await GraphTypeDefinitions.RoleTypeGQLModel.resolve_reference(info, self.roletype_id)
        return result

    @strawberry.field(
        description="""User having this role. Must be member of group?"""
    )
    async def user(self, info: strawberry.types.Info) -> UserGQLModel:
        # result = await resolveUserById(session,  self.user_id)
        result = await GraphTypeDefinitions.UserGQLModel.resolve_reference(info, self.user_id)
        return result

    @strawberry.field(description="""Group where user has a role name""")
    async def group(self, info: strawberry.types.Info) -> GroupGQLModel:
        # result = await resolveGroupById(session,  self.group_id)
        result = await GraphTypeDefinitions.GroupGQLModel.resolve_reference(info, self.group_id)
        return result
    
#####################################################################
#
# Special fields for query
#
#####################################################################

#####################################################################
#
# Mutation section
#
#####################################################################
import datetime

@strawberry.input(description="""Input model for updating a role""")
class RoleUpdateGQLModel:
    id: uuid.UUID
    lastchange: datetime.datetime
    valid: Optional[bool] = None
    startdate: Optional[datetime.datetime] = None
    enddate: Optional[datetime.datetime] = None

@strawberry.input(description="""Input model for inserting a new role""")
class RoleInsertGQLModel:
    user_id: uuid.UUID
    group_id: uuid.UUID
    roletype_id: uuid.UUID
    id: Optional[uuid.UUID] = None
    valid: Optional[bool] = True
    startdate: Optional[datetime.datetime] = datetime.datetime.now()
    enddate: Optional[datetime.datetime] = None

@strawberry.input(description="""Input model for deleting a role""")
class RoleDeleteGQLModel:
    id: uuid.UUID

@strawberry.type(description="""Result model for role operations""")
class RoleResultGQLModel:
    id: uuid.UUID = None
    msg: str = None

    @strawberry.field(description="""Result of user operation""")
    async def role(self, info: strawberry.types.Info) -> Union[RoleGQLModel, None]:
        result = await RoleGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberry.type(description="""Result model for role deletion""")
class RoleDeleteResultGQLModel:
    id: uuid.UUID = None
    msg: str = None

    @strawberry.field(description="""Result of role deletion""")
    async def role(self, info: strawberry.types.Info) -> Union[RoleGQLModel, None]:
        # Assuming you have a resolve_reference function for retrieving deleted role details
        result = await RoleGQLModel.resolve_reference(info, self.id)
        return result

@strawberry.mutation(description="""Updates a role""")
async def role_update(self, 
    info: strawberry.types.Info, 
    role: RoleUpdateGQLModel
) -> RoleResultGQLModel:

    loader = getLoader(info).roles
    updatedrow = await loader.update(role)

    result = RoleResultGQLModel()
    result.msg = "ok"
    result.id = role.id
    
    if updatedrow is None:
        result.msg = "fail"        
    
    return result

@strawberry.mutation(description="""Inserts a role""")
async def role_insert(self, 
    info: strawberry.types.Info, 
    role: RoleInsertGQLModel
) -> RoleResultGQLModel:

    loader = getLoader(info).roles

    result = RoleResultGQLModel()
    result.msg = "ok"
    
    updatedrow = await loader.insert(role)
    result.id = updatedrow.id
    
    return result

@strawberry.mutation(description="""Deletes a role""")
async def role_delete(self, info: strawberry.types.Info, role: RoleDeleteGQLModel) -> RoleDeleteResultGQLModel:
    loader = getLoader(info).roles

    # Perform role deletion operation
    deleted_row = await loader.delete(role.id)

    result = RoleDeleteResultGQLModel()
    result.id = role.id

    if deleted_row is None:
        result.msg = "fail"
    else:
        result.msg = "ok"

    return result