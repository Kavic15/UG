import logging
from uoishelpers.dataloaders import createIdLoader, createFkeyLoader


from DBDefinitions import (
    UserModel,
    MembershipModel,
    GroupModel,
    GroupTypeModel,
    RoleModel,
    RoleTypeModel,
    RoleCategoryModel
)


async def _createLoaders(
    asyncSessionMaker,
    DBModels=[
        UserModel,
        MembershipModel,
        GroupModel,
        GroupTypeModel,
        RoleModel,
        RoleTypeModel,
        RoleCategoryModel,
    ],
):

    modelIndex = dict((DBModel.__tablename__, DBModel) for DBModel in DBModels)

    result = {}
    for tableName, DBModel in modelIndex.items():  # iterate over all models
        result[tableName] = createIdLoader(asyncSessionMaker, DBModel)
    # result['memberships'].max_batch_size = 20
    return result

dbmodels = {
    "users": UserModel,
    "memberships": MembershipModel,
    "groups": GroupModel,
    "grouptypes": GroupTypeModel,
    "roles": RoleModel,
    "roletypes": RoleTypeModel,
    "rolecategories": RoleCategoryModel,
}

class Loaders:
    users = None
    groups = None
    memberships = None
    grouptypes = None
    roles = None
    roletypes = None
    rolecategories = None
    roletypelists = None
    pass

async def createLoaders(asyncSessionMaker, models=dbmodels):
    def createLambda(loaderName, DBModel):
        return lambda self: createIdLoader(asyncSessionMaker, DBModel)
    
    attrs = {}
    for key, DBModel in models.items():
        attrs[key] = property(cache(createLambda(key, DBModel)))
    
    Loaders = type('Loaders', (), attrs)   
    return Loaders()

from functools import cache

# async def createLoaders_2(
#     asyncSessionMaker,
#     DBModels = [UserModel, MembershipModel, GroupModel, GroupTypeModel, RoleModel, RoleTypeModel],
#     FKeyedDBModels = {}
#     ):

#     def IdLoader(DBModel):
#         @property
#         @cache
#         def getIt(self):
#             return createIdLoader(asyncSessionMaker, DBModel)

#     def keyedLoader(DBModel, foreignKeyName):
#         @property
#         @cache
#         def getIt(self):
#             return createFkeyLoader(asyncSessionMaker, DBModel, foreignKeyName=foreignKeyName)


#     modelIndex = dict((DBModel.__tablename__, DBModel) for DBModel in DBModels)
#     revIndex = dict((DBModel, DBModel.__tablename__) for DBModel in DBModels)

#     attrs = {}
#     for tableName, DBModel in modelIndex.items():  # iterate over all models
#         attrs[tableName] = IdLoader(DBModel)

#     for DBModel, fkeyNames in FKeyedDBModels.items():
#         tableName = revIndex[DBModel]
#         for fkeyName in fkeyNames:
#             name = tableName + '_' + fkeyName
#             attrs[name] = keyedLoader(DBModel, fkeyName)

#     result = type("loaders", (object, ), attrs)
#     #result = type("resolvers", (object, ), {'experiment': experiment, 'loader_a': experiment})
#     return result()


async def createLoaders_3(asyncSessionMaker):
    class Loaders:
        @property
        @cache
        def users(self):
            return createIdLoader(asyncSessionMaker, UserModel)

        @property
        @cache
        def groups(self):
            return createIdLoader(asyncSessionMaker, GroupModel)

        @property
        @cache
        def roles(self):
            return createIdLoader(asyncSessionMaker, RoleModel)

        @property
        @cache
        def roles_for_user_id(self):
            return createFkeyLoader(asyncSessionMaker, RoleModel, foreignKeyName="user_id")

        @property
        @cache
        def roletypes(self):
            return createIdLoader(asyncSessionMaker, RoleTypeModel)

        @property
        @cache
        def grouptypes(self):
            return createIdLoader(asyncSessionMaker, GroupTypeModel)

        @property
        @cache
        def memberships(self):
            return createIdLoader(asyncSessionMaker, MembershipModel)

        @property
        @cache
        def memberships_user_id(self):
            return createFkeyLoader(
                asyncSessionMaker, MembershipModel, foreignKeyName="user_id"
            )

        @property
        @cache
        def memberships_group_id(self):
            return createFkeyLoader(
                asyncSessionMaker, MembershipModel, foreignKeyName="group_id"
            )

        @property
        @cache
        def groups_mastergroup_id(self):
            return createFkeyLoader(
                asyncSessionMaker, GroupModel, foreignKeyName="mastergroup_id"
            )

    return Loaders()

demouser = {
    "id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
    "name": "John",
    "surname": "Newbie",
    "email": "john.newbie@world.com",
    "roles": [
        {
            "valid": True,
            "group": {
                "id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
                "name": "Uni"
            },
            "roletype": {
                "id": "ced46aa4-3217-4fc1-b79d-f6be7d21c6b6",
                "name": "administrátor"
            }
        },
        {
            "valid": True,
            "group": {
                "id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
                "name": "Uni"
            },
            "roletype": {
                "id": "ae3f0d74-6159-11ed-b753-0242ac120003",
                "name": "rektor"
            }
        }
    ]
}

def getUserFromInfo(info):
    context = info.context
    #print(list(context.keys()))
    result = context.get("user", None)
    if result is None:
        request = context.get("request", None)
        assert request is not None, context
        result = request.scope["user"]

    if result is None:
        result = {"id": None}
    else:
        result = {**result, "id": uuid.UUID(result["id"])}
    logging.debug("getUserFromInfo", result)
    return result

def getLoadersFromInfo(info) -> Loaders:
    context = info.context
    loaders = context["all"]
    return loaders

async def createLoadersContext(asyncSessionMaker):
    return {
        "loaders": await createLoaders(asyncSessionMaker)
    }
