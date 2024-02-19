import datetime
import aiohttp
import asyncio
import logging
from sqlalchemy import select
from functools import cache
import os
from uoishelpers.dataloaders import createIdLoader, createFkeyLoader
from aiodataloader import DataLoader

from gql_ug.DBDefinitions import (
    UserModel,
    MembershipModel,
    GroupModel,
    GroupTypeModel,
    RoleModel,
    RoleTypeModel,
    RoleCategoryModel
)

dbmodels = {
    "users": UserModel,
    "memberships": MembershipModel,
    "groups": GroupModel,
    "grouptypes": GroupTypeModel,
    "roles": RoleModel,
    "roletypes": RoleTypeModel,
    "rolecategories": RoleCategoryModel
}

class Loaders:
    users = None
    groups = None
    memberships = None
    grouptypes = None
    roles = None
    roletypes = None
    rolecategories = None
    pass

def createLoaders(asyncSessionMaker, models=dbmodels) -> Loaders:
    def createLambda(loaderName, DBModel):
        return lambda self: createIdLoader(asyncSessionMaker, DBModel)
    
    attrs = {}
    for key, DBModel in models.items():
        attrs[key] = property(cache(createLambda(key, DBModel)))
    
    Loaders = type('Loaders', (), attrs)   
    return Loaders()

from functools import cache

@cache
def composeAuthUrl():
    hostname = os.environ.get("AUTHURL", "http://localhost:8088/gql")
    assert "://" in hostname, "probably bad formated url, has it 'protocol' part?"
    assert "." not in hostname, "security check failed, change source code"
    return hostname


class AuthorizationLoader(DataLoader):

    query = """query($id: UUID!){result: rbacById(id: $id) {roles {user { id } group { id } roletype { id }}}}"""
            # variables = {"id": rbacobject}

    roleUrlEndpoint=None#composeAuthUrl()
    def __init__(self,
        roleUrlEndpoint=roleUrlEndpoint,
        query=query,
        demo=True):
        super().__init__(cache=True)
        self.roleUrlEndpoint = roleUrlEndpoint if roleUrlEndpoint else composeAuthUrl()
        self.query = query
        self.demo = demo
        self.authorizationToken = ""

    def setTokenByInfo(self, info):
        self.authorizationToken = ""

    async def _load(self, id):
        variables = {"id": f"{id}"}
        if self.authorizationToken != "":
            headers = {"authorization": f"Bearer {self.authorizationToken}"}
        else:
            headers = {}
        json = {
            "query": self.query,
            "variables": variables
        }
        roleUrlEndpoint=self.roleUrlEndpoint
        async with aiohttp.ClientSession() as session:
            print(f"query {roleUrlEndpoint} for json={json}")
            async with session.post(url=roleUrlEndpoint, json=json, headers=headers) as resp:
                print(resp.status)
                if resp.status != 200:
                    text = await resp.text()
                    print(text)
                    return []
                else:
                    respJson = await resp.json()

        # print(20*"respJson")
        # print(respJson)
        
        assert respJson.get("errors", None) is None, respJson["errors"]
        respdata = respJson.get("data", None)
        assert respdata is not None, "missing data response"
        result = respdata.get("result", None)
        assert result is not None, "missing result"
        roles = result.get("roles", None)
        assert roles is not None, "missing roles"
        
        # print(30*"=")
        # print(roles)
        # print(30*"=")
        return [*roles]


    async def batch_load_fn(self, keys):
        #print('batch_load_fn', keys, flush=True)
        reducedkeys = set(keys)
        awaitables = (self._load(key) for key in reducedkeys)
        results = await asyncio.gather(*awaitables)
        indexedResult = {key:result for key, result in zip(reducedkeys, results)}
        results = [indexedResult[key] for key in keys]
        return results

def update(destination, source=None, extraValues={}):
    """Updates destination's attributes with source's attributes.
    Attributes with value None are not updated."""
    if source is not None:
        for name in dir(source):
            if name.startswith("_"):
                continue
            value = getattr(source, name)
            if value is not None:
                setattr(destination, name, value)

    for name, value in extraValues.items():
        setattr(destination, name, value)

    return destination

def createLoaders(asyncSessionMaker):
    class Loaders:
        
        @property
        @cache
        def users(self):
            return createIdLoader(asyncSessionMaker, UserModel)
        
        @property
        @cache
        def memberships(self):
            return createIdLoader(asyncSessionMaker, MembershipModel)
        
        @property
        @cache
        def memberships_user_id(self):
            return createFkeyLoader(asyncSessionMaker, MembershipModel, foreignKeyName="user_id")
        
        @property
        @cache
        def groups(self):
            return createIdLoader(asyncSessionMaker, GroupModel)
        
        @property
        @cache
        def grouptypes(self):
            return createIdLoader(asyncSessionMaker, GroupTypeModel)
        
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
        def rolecategories(self):
            return createIdLoader(asyncSessionMaker, RoleCategoryModel)
        
        @property
        @cache
        def authorizations(self):
            return AuthorizationLoader()
        
        @property
        @cache
        def groups_mastergroup_id(self):
            return createFkeyLoader(
                asyncSessionMaker, GroupModel, foreignKeyName="mastergroup_id"
            )

    return Loaders()

def getLoadersFromInfo(info) -> Loaders:
     context = info.context
     loaders = context.get("loaders", None)
     assert loaders is not None, "loaders není v kontextu"
     return loaders
    #return info.context['all']

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
    user = context.get("user", None)
    if user is None:
        request = context.get("request", None)
        assert request is not None, "request is missing in context :("
        user = request.scope.get("user", None)
        assert user is not None, "missing user in context or in request.scope"
    logging.debug("getUserFromInfo", user)
    return user

def getAuthorizationToken(info):
    context = info.context
    request = context.get("request", None)
    assert request is not None, "trying to get authtoken from None request"

def createUgConnectionContext(request):
    from .gql_ug_proxy import get_ug_connection
    connection = get_ug_connection(request=request)
    return {
        "ug_connection": connection
    }

def getUgConnection(info):
    context = info.context
    print("getUgConnection.context", context)
    connection = context.get("ug_connection", None)
    return connection

def createLoadersContext(asyncSessionMaker):
    return {
        "loaders": createLoaders(asyncSessionMaker)
    }
