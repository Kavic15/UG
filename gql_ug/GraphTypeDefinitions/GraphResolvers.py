import strawberry
import uuid
import datetime
import typing
import logging

from inspect import signature
import inspect 
from functools import wraps
from gql_ug.GraphPermissions import OnlyForAuthentized

UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".userGQLModel")]
GroupGQLModel = typing.Annotated["GroupGQLModel", strawberry.lazy(".groupGQLModel")]
RoleTypeGQLModel = typing.Annotated["RoleTypeGQLModel", strawberry.lazy(".roleGQLModel")]

@strawberry.field(description="""Entity primary key""", permission_classes=[OnlyForAuthentized()])
def resolve_id(self) -> uuid.UUID:
    return self.id

@strawberry.field(description="""Name """, permission_classes=[OnlyForAuthentized()])
def resolve_name(self) -> str:
    return self.name

@strawberry.field(description="""Time of last update""", permission_classes=[OnlyForAuthentized()])
def resolve_lastchange(self) -> datetime.datetime:
    return self.lastchange

@strawberry.field(description="""English name""", permission_classes=[OnlyForAuthentized()])
def resolve_name_en(self) -> str:
    result = self.name_en if self.name_en else ""
    return result

@strawberry.field(description="""Start date""")
def resolve_startdate(self) -> datetime.date:
    return self.startdate

@strawberry.field(description="""End date""")
def resolve_enddate(self) -> datetime.date:
    return self.enddate

@strawberry.field(description="""Validity""")
def resolve_valid(self) -> bool:
    return self.valid


async def resolve_group(group_id):
    from GraphTypeDefinitions import GroupGQLModel
    result = None if group_id is None else await GroupGQLModel.resolve_reference(group_id)
    return result


@strawberry.field(description="""Group ID""", permission_classes=[OnlyForAuthentized()])
async def resolve_group_id(self) -> typing.Optional["GroupGQLModel"]:
    return await resolve_group(self.group_id)


async def resolve_user(user_id):
    from .userGQLModel import UserGQLModel
    result = None if user_id is None else await UserGQLModel.resolve_reference(user_id)
    return result


@strawberry.field(description="""User ID """, permission_classes=[OnlyForAuthentized()])
async def resolve_user_id(self) -> typing.Optional["UserGQLModel"]:
    return await resolve_user(self.user_id)


async def resolve_roletype(roletype_id):
    from GraphTypeDefinitions import RoleTypeGQLModel
    result = None if roletype_id is None else await RoleTypeGQLModel.resolve_reference(roletype_id)
    return result

@strawberry.field(description="""Role Type ID """, permission_classes=[OnlyForAuthentized()])
async def resolve_roletype_id(self) -> typing.Optional["RoleTypeGQLModel"]:
    return await resolve_roletype(self.roletype_id)


@strawberry.field(description="""Level of authorization""", permission_classes=[OnlyForAuthentized()])
def resolve_accesslevel(self) -> int:
    return self.accesslevel


@strawberry.field(description="""Time of entity introduction""",permission_classes=[OnlyForAuthentized()])
def resolve_created(self) -> typing.Optional[datetime.datetime]:
    return self.created


@strawberry.field(description="""Who created entity""", permission_classes=[OnlyForAuthentized()])
async def resolve_createdby(self) -> typing.Optional["UserGQLModel"]:
    return await resolve_user(self.created_by)


@strawberry.field(description="""Who made last change""", permission_classes=[OnlyForAuthentized()])
async def resolve_changedby(self) -> typing.Optional["UserGQLModel"]:
    return await resolve_user(self.changedby)


RBACObjectGQLModel = typing.Annotated["RBACObjectGQLModel", strawberry.lazy(".RBACObjectGQLModel")]
@strawberry.field(description="""Who made last change""", permission_classes=[OnlyForAuthentized()])
async def resolve_rbacobject(self, info: strawberry.types.Info) -> typing.Optional[RBACObjectGQLModel]:
    from .RBACObjectGQLModel import RBACObjectGQLModel
    result = None if self.rbacobject is None else await RBACObjectGQLModel.resolve_reference(info, self.rbacobject)
    return result


resolve_result_id: uuid.UUID = strawberry.field(description="primary key of CU operation object")
resolve_result_msg: str = strawberry.field(description="""Should be `ok` if descired state has been reached, otherwise `fail`.
For update operation fail should be also stated when bad lastchange has been entered.""")

# fields for mutations insert and update
resolve_insert_id = strawberry.field(graphql_type=typing.Optional[uuid.UUID], description="primary key (UUID), could be client generated", default=None)
resolve_update_id = strawberry.field(graphql_type=uuid.UUID, description="primary key (UUID), identifies object of operation")
resolve_update_lastchage = strawberry.field(graphql_type=datetime.datetime, description="timestamp of last change = TOKEN")

# fields for mutation result
resolve_cu_result_id = strawberry.field(graphql_type=uuid.UUID, description="primary key of CU operation object",
    permission_classes=[OnlyForAuthentized()])
resolve_cu_result_msg = strawberry.field(graphql_type=str, description="""Should be `ok` if descired state has been reached, otherwise `fail`.
For update operation fail should be also stated when bad lastchange has been entered.""",
    permission_classes=[OnlyForAuthentized()])


#---byID---#
def createByIdResolver(
    scalarType: None = None,
    foreignKeyName: str = None,
    description="Retrieves item by its id",
    permission_classes=()
):
    assert scalarType is not None
    assert foreignKeyName is not None

    @strawberry.field(description=description, permission_classes=permission_classes)
    async def foreignkeyScalar(
        self, info: strawberry.types.Info
    ) -> typing.Optional[scalarType]:
        # 👇 self must have an attribute, otherwise it is fail of definition
        assert hasattr(self, foreignKeyName)
        id = getattr(self, foreignKeyName, None)

        result = None if id is None else await scalarType.resolve_reference(info=info, id=id)
        return result

    return foreignkeyScalar

#---asPAGE---#
def createAsPageResolver(
    scalarType: None = None,
    whereFilterType: None = None,
    foreignKeyName: str = None,
    loaderLambda=lambda info: None,
    description="Retrieves items paged",
    skip: int = 0,
    limit: int = 10):
    assert scalarType is not None
    assert foreignKeyName is not None

    @strawberry.field(description=description)
    async def foreignkeyVector(
            self, info: strawberry.types.Info,
            skip: int = skip,
            limit: int = limit,
            where: typing.Optional[whereFilterType] = None
    ) -> typing.List[scalarType]:
        params = {foreignKeyName: self.id}
        loader = loaderLambda(info)
        assert loader is not None

        wf = None if where is None else strawberry.asdict(where)
        result = await loader.page(skip=skip, limit=limit, where=wf, extendedfilter=params)
        return result

    return foreignkeyVector


def createRootResolver_by_id(scalarType: None, description="Retrieves item by its id"):
    assert scalarType is not None
    @strawberry.field(description=description,
    permission_classes=[OnlyForAuthentized()])
    async def by_id(
        self, info: strawberry.types.Info, id: uuid.UUID
    ) -> typing.Optional[scalarType]:
        result = await scalarType.resolve_reference(info=info, id=id)
        return result
    return by_id


def createRootResolver_by_page(
    scalarType: None, 
    whereFilterType: None,
    loaderLambda = lambda info: None, 
    description="Retrieves items paged", 
    skip: int=0, 
    limit: int=10,
    orderby: typing.Optional[str] = None,
    desc: typing.Optional[bool] = None):

    assert scalarType is not None
    assert whereFilterType is not None
    
    @strawberry.field(description=description,
    permission_classes=[OnlyForAuthentized()])
    async def paged(
        self, info: strawberry.types.Info, 
        skip: int=skip, limit: int=limit, where: typing.Optional[whereFilterType] = None,
        orderby: typing.Optional[str] = None
    ) -> typing.List[scalarType]:
        loader = loaderLambda(info)
        assert loader is not None
        wf = None if where is None else strawberry.asdict(where)
        result = await loader.page(skip=skip, limit=limit, where=wf, orderby=orderby, desc=desc)
        return result
    return paged
