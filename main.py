# from fastapi import FastAPI
# from DBDefinitions import startEngine, ComposeConnectionString

# ## Zabezpecuje prvotni inicializaci DB a definovani Nahodne struktury pro "Univerzity"
# from utils.DBFeeder import initDB

# connectionString = ComposeConnectionString()


# def singleCall(asyncFunc):
#     """Dekorator, ktery dovoli, aby dekorovana funkce byla volana (vycislena) jen jednou. Navratova hodnota je zapamatovana a pri dalsich volanich vracena.
#     Dekorovana funkce je asynchronni.
#     """
#     resultCache = {}

#     async def result():
#         if resultCache.get("result", None) is None:
#             resultCache["result"] = await asyncFunc()
#         return resultCache["result"]

#     return result


# @singleCall
# async def RunOnceAndReturnSessionMaker():
#     """Provadi inicializaci asynchronniho db engine, inicializaci databaze a vraci asynchronni SessionMaker.
#     Protoze je dekorovana, volani teto funkce se provede jen jednou a vystup se zapamatuje a vraci se pri dalsich volanich.
#     """
#     print(f'starting engine for "{connectionString}"')

#     import os
#     makeDrop = os.environ.get("DEMO", "") == "true"
#     result = await startEngine(
#         connectionstring=connectionString, makeDrop=makeDrop, makeUp=True
#     )

#     print(f"initializing system structures")
#     ###########################################################################################################################
#     #
#     # zde definujte do funkce asyncio.gather
#     # vlozte asynchronni funkce, ktere maji data uvest do prvotniho konzistentniho stavu
#     await initDB(result)
#     # await asyncio.gather( # concurency running :)
#     # sem lze dat vsechny funkce, ktere maji nejak inicializovat databazi
#     # musi byt asynchronniho typu (async def ...)
#     # createSystemDataStructureRoleTypes(result),
#     # createSystemDataStructureGroupTypes(result)
#     # )

#     ###########################################################################################################################
#     print(f"all done")
#     return result


# from strawberry.asgi import GraphQL
# from utils.Dataloaders import createLoaders, createLoaders_3


# async def createContext():
#     asyncSessionMaker = await RunOnceAndReturnSessionMaker()
#     loaders = await createLoaders(asyncSessionMaker)
#     return {
#         "asyncSessionMaker": await RunOnceAndReturnSessionMaker(),
#         "all": await createLoaders(asyncSessionMaker),
#         #**loaders,
#     }


# class MyGraphQL(GraphQL):
#     """Rozsirena trida zabezpecujici praci se session"""

#     async def __call__(self, scope, receive, send):
#         # print("another gql call (ug)")
#         # for item in scope['headers']:
#         #    print(item)
#         self._user = { "id": "f8089aa6-2c4a-4746-9503-105fcc5d054c" }
#         result = await GraphQL.__call__(self, scope, receive, send)
#         return result

#     async def get_context(self, request, response):
#         parentResult = await GraphQL.get_context(self, request, response)
#         localResult = await createContext()
#         return {**parentResult, **localResult, "user": self._user}


# from GraphTypeDefinitions import schema

# ## ASGI app, kterou "moutneme"
# graphql_app = MyGraphQL(
#     # strawberry.federation.Schema(Query),
#     schema,
#     graphiql=True,
#     allow_queries_via_get=True,
# )

# app = FastAPI()
# app.mount("/gql", graphql_app)

# @app.on_event("startup")
# async def startup_event():
#     initizalizedEngine = await RunOnceAndReturnSessionMaker()
#     return None


# print("All initialization is done")

import logging
import os
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from strawberry.fastapi import GraphQLRouter
from contextlib import asynccontextmanager

from DBDefinitions import startEngine, ComposeConnectionString

# import socket
# import logging
# import logging.config
# import logging.handlers
# import yaml
# logging.socket = socket
# with open('./logging.yaml', 'r') as stream:
#     # Converts yaml document to python object
#     config = yaml.safe_load(stream)
#     print(config)
#     logging.config.dictConfig(config)
# logging.config.d("./logging.yaml", disable_existing_loggers=False)



import logging
import logging.handlers
import socket
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s.%(msecs)03d\t%(levelname)s:\t%(message)s', 
    datefmt='%Y-%m-%dT%I:%M:%S')
SYSLOGHOST = os.getenv("SYSLOGHOST", None)
if SYSLOGHOST is not None:
    [address, strport, *_] = SYSLOGHOST.split(':')
    assert len(_) == 0, f"SYSLOGHOST {SYSLOGHOST} has unexpected structure, try `localhost:514` or similar (514 is UDP port)"
    port = int(strport)
    my_logger = logging.getLogger()
    my_logger.setLevel(logging.INFO)
    handler = logging.handlers.SysLogHandler(address=(address, port), socktype=socket.SOCK_DGRAM)
    #handler = logging.handlers.SocketHandler('10.10.11.11', 611)
    my_logger.addHandler(handler)


## Zabezpecuje prvotni inicializaci DB a definovani Nahodne struktury pro "Univerzity"
from utils.DBFeeder import initDB

connectionString = ComposeConnectionString()

appcontext = {}
@asynccontextmanager
async def initEngine(app: FastAPI):

    from DBDefinitions import startEngine, ComposeConnectionString

    connectionstring = ComposeConnectionString()

    asyncSessionMaker = await startEngine(
        connectionstring=connectionstring,
        makeDrop=True,
        makeUp=True
    )

    appcontext["asyncSessionMaker"] = asyncSessionMaker

    logging.info("engine started")

    from utils.DBFeeder import initDB
    await initDB(asyncSessionMaker)

    logging.info("data (if any) imported")
    yield


from GraphTypeDefinitions import schema
async def get_context(request: Request):
    asyncSessionMaker = appcontext.get("asyncSessionMaker", None)
    if asyncSessionMaker is None:
        async with initEngine(app) as cntx:
            pass
        
    from utils.Dataloaders import createLoadersContext
    context = createLoadersContext(appcontext["asyncSessionMaker"])
    result = {**context}
    result["request"] = request
    result["user"] = request.scope.get("user", None)
    logging.info(f"context created {result}")

    return {**context}

app = FastAPI(lifespan=initEngine)

from doc import attachVoyager
attachVoyager(app, path="/gql/doc")


print("All initialization is done")
@app.get('/hello')
def hello(request: Request):
    headers = request.headers
    auth = request.auth
    user = request.scope["user"]
    return {'hello': 'world', 'headers': {**headers}, 'auth': f"{auth}", 'user': user}

JWTPUBLICKEYURL = os.environ.get("JWTPUBLICKEYURL", "http://localhost:8000/oauth/publickey")
JWTRESOLVEUSERPATHURL = os.environ.get("JWTRESOLVEUSERPATHURL", "http://localhost:8000/oauth/userinfo")

class Item(BaseModel):
    query: str
    variables: dict = None
    operationName: str = None

apolloQuery = "query __ApolloGetServiceDefinition__ { _service { sdl } }"
graphiQLQuery = "\n    query IntrospectionQuery {\n      __schema {\n        \n        queryType { name }\n        mutationType { name }\n        subscriptionType { name }\n        types {\n          ...FullType\n        }\n        directives {\n          name\n          description\n          \n          locations\n          args(includeDeprecated: true) {\n            ...InputValue\n          }\n        }\n      }\n    }\n\n    fragment FullType on __Type {\n      kind\n      name\n      description\n      \n      fields(includeDeprecated: true) {\n        name\n        description\n        args(includeDeprecated: true) {\n          ...InputValue\n        }\n        type {\n          ...TypeRef\n        }\n        isDeprecated\n        deprecationReason\n      }\n      inputFields(includeDeprecated: true) {\n        ...InputValue\n      }\n      interfaces {\n        ...TypeRef\n      }\n      enumValues(includeDeprecated: true) {\n        name\n        description\n        isDeprecated\n        deprecationReason\n      }\n      possibleTypes {\n        ...TypeRef\n      }\n    }\n\n    fragment InputValue on __InputValue {\n      name\n      description\n      type { ...TypeRef }\n      defaultValue\n      isDeprecated\n      deprecationReason\n    }\n\n    fragment TypeRef on __Type {\n      kind\n      name\n      ofType {\n        kind\n        name\n        ofType {\n          kind\n          name\n          ofType {\n            kind\n            name\n            ofType {\n              kind\n              name\n              ofType {\n                kind\n                name\n                ofType {\n                  kind\n                  name\n                  ofType {\n                    kind\n                    name\n                  }\n                }\n              }\n            }\n          }\n        }\n      }\n    }\n  "
roleTypeQuery = "{roleTypePage(limit: 1000) {id, name, nameEn}}"
from uoishelpers.authenticationMiddleware import createAuthentizationSentinel
sentinel = createAuthentizationSentinel(
    JWTPUBLICKEY=JWTPUBLICKEYURL,
    JWTRESOLVEUSERPATH=JWTRESOLVEUSERPATHURL,
    queriesWOAuthentization=[apolloQuery, graphiQLQuery, roleTypeQuery],
    onAuthenticationError=lambda item: JSONResponse({"data": None, "errors": ["Unauthenticated", item.query, f"{item.variables}"]}, 
    status_code=401))

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context
)

@app.get("/gql")
async def graphiql(request: Request):
    return await graphql_app.render_graphql_ide(request)

import time
@app.post("/gql")
async def apollo_gql(request: Request, item: Item):
    DEMOE = os.getenv("DEMO", None)

    sentinelResult = await sentinel(request, item)

    logging.info(f"asking sentinel for advice (is user authenticated?)")
    if DEMOE == "False":
        if sentinelResult:
            return sentinelResult
        
    start = time.perf_counter()
    try:
        context = await get_context(request)
        if DEMOE == "True":
            if context.get("user", None) is None:
                context["user"] = {"id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003"}
                
        schemaresult = await schema.execute(item.query, variable_values=item.variables, operation_name=item.operationName, context_value=context)
        # assert 1 == 0, ":)"
    except Exception as e:
        return {"data": None, "errors": [f"{type(e).__name__}: {e}"]}
    
    duration = time.perf_counter() - start
    print(f"query duration {duration/1000} ms" )
    
    result = {"data": schemaresult.data}
    if schemaresult.errors:
        result["errors"] = [f"{error}" for error in schemaresult.errors]
    return result

# from uoishelpers.authenticationMiddleware import BasicAuthenticationMiddleware302, BasicAuthBackend
# app.add_middleware(BasicAuthenticationMiddleware302, backend=BasicAuthBackend(
#         JWTPUBLICKEY = JWTPUBLICKEY,
#         JWTRESOLVEUSERPATH = JWTRESOLVEUSERPATH
# ))

import os
DEMO = os.getenv("DEMO", None)
assert DEMO is not None, "DEMO environment variable must be explicitly defined"
assert (DEMO == "True") or (DEMO == "False"), "DEMO environment variable can have only `True` or `False` values"
DEMO = DEMO == "True"

if DEMO:
    print("####################################################")
    print("#                                                  #")
    print("# RUNNING IN DEMO                                  #")
    print("#                                                  #")
    print("####################################################")

    logging.info("####################################################")
    logging.info("#                                                  #")
    logging.info("# RUNNING IN DEMO                                  #")
    logging.info("#                                                  #")
    logging.info("####################################################")