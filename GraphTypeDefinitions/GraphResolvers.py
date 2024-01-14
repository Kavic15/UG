# from typing import Coroutine, Callable, Awaitable, Union, List
# import uuid
# from sqlalchemy.future import select
# from sqlalchemy.orm import selectinload, joinedload
# from sqlalchemy.ext.asyncio import AsyncSession

# from uoishelpers.resolvers import (
#     create1NGetter,
#     createEntityByIdGetter,
#     createEntityGetter,
#     createInsertResolver,
#     createUpdateResolver,
# )
# from uoishelpers.resolvers import putSingleEntityToDb

# from DBDefinitions import (
#     BaseModel,
#     UserModel,
#     GroupModel,
#     MembershipModel,
#     RoleModel,
# )
# from DBDefinitions import GroupTypeModel, RoleTypeModel


# ## Dataloaders

# userSelect = select(UserModel)
# userIdIn = UserModel.id.in_
# groupSelect = select(GroupModel)
# groupTypeSelect = select(GroupTypeModel)
# membershipsSelect = select(MembershipModel)
# roleSelect = select(RoleModel)
# roleTypeSelect = select(RoleTypeModel)



# import strawberry
# from strawberry.dataloader import DataLoader

# # async def load_users(keys: List[int]) -> List[User]:
# #    return [User(id=key) for key in keys]
# # loader = DataLoader(load_fn=load_users)


# def createEntityByIdListGetter(DBModel):
#     async def resultFunc(session, keys):
#         result = {}
#         statement = select(DBModel).filter(DBModel.id.in_(keys))
#         rows = await session.execute(statement)
#         rows = list(rows.scalars())
#         for item in rows:
#             result[f"{item.id}"] = item

#         resultList = [result.get(id, None) for id in keys]
        
#         # print(DBModel, 'resultList', resultList, flush=True)
#         # print(DBModel, 'ids', [item.id for item in rows], flush=True)
#         return resultList

#     return resultFunc


# # resolveUsersById = createEntityByIdListGetter(UserModel)
# # resolveGroupsById = createEntityByIdListGetter(GroupModel)


# def createDataLoaderResolver(definitions):
#     def bind(asyncSessionMaker, DataLoader=DataLoader):
#         def createSingleLoader(DBModel, GQLModel):
#             async def loader(keys: List[uuid.UUID]) -> List[GQLModel]:
#                 print("query", DBModel, "for keys", keys, flush=True)
#                 statement = select(DBModel).filter(DBModel.id.in_(keys))
#                 async with asyncSessionMaker() as session:
#                     rows = await session.execute(statement)
#                     result = rows.scalars()
#                     return result

#             return loader

#         result = {}
#         for key, value in definitions.items():
#             loader = createSingleLoader(value["DBModel"], value["GQLModel"])
#             result[key] = DataLoader(load_fn=loader)
#         return result

#     return bind


# ## Nasleduji funkce, ktere lze pouzit jako asynchronni resolvery
# ## user resolvers
# resolveUserById = createEntityByIdGetter(UserModel)
# resolveUserAll = createEntityGetter(UserModel)
# resolveMembershipForUser = create1NGetter(
#     MembershipModel, foreignKeyName="user_id", options=joinedload(MembershipModel.group)
# )
# resolveRolesForUser = create1NGetter(
#     RoleModel, foreignKeyName="user_id", options=joinedload(RoleModel.roletype)
# )

# resolverUpdateUser = createUpdateResolver(UserModel, safe=True)
# resolveInsertUser = createInsertResolver(UserModel)


# async def resolveUsersByThreeLetters(
#     session: AsyncSession, validity=None, letters: str = ""
# ) -> List[UserModel]:
#     if len(letters) < 3:
#         return []
#     stmt = select(UserModel).where(
#         (UserModel.name + " " + UserModel.surname).like(f"%{letters}%")
#     )
#     if validity is not None:
#         stmt = stmt.filter_by(valid=True)

#     dbSet = await session.execute(stmt)
#     return dbSet.scalars()


# ## group resolvers
# resolveGroupById = createEntityByIdGetter(GroupModel)
# resolveGroupAll = createEntityGetter(GroupModel)
# resolveMembershipForGroup = create1NGetter(
#     MembershipModel, foreignKeyName="group_id", options=joinedload(MembershipModel.user)
# )
# resolveSubgroupsForGroup = create1NGetter(GroupModel, foreignKeyName="mastergroup_id")
# resolveMastergroupForGroup = createEntityByIdGetter(GroupModel)
# resolveRolesForGroup = create1NGetter(RoleModel, foreignKeyName="group_id")

# resolveUpdateGroup = createUpdateResolver(GroupModel, safe=True)
# resolveInsertGroup = createInsertResolver(GroupModel)


# async def resolveGroupsByThreeLetters(
#     session: AsyncSession, validity=None, letters: str = ""
# ) -> List[GroupModel]:
#     if len(letters) < 3:
#         return []
#     stmt = select(GroupModel).where(GroupModel.name.like(f"%{letters}%"))
#     if validity is not None:
#         stmt = stmt.filter_by(valid=True)

#     dbSet = await session.execute(stmt)
#     return dbSet.scalars()


# ## membership resolvers
# resolveUpdateMembership = createUpdateResolver(MembershipModel)
# resolveInsertMembership = createInsertResolver(MembershipModel)
# resolveMembershipById = createEntityByIdGetter(MembershipModel)

# # grouptype resolvers
# resolveGroupTypeById = createEntityByIdGetter(GroupTypeModel)
# resolveGroupTypeAll = createEntityGetter(GroupTypeModel)
# selectGroup = select(GroupModel)
# selectGroupType= select(GroupTypeModel)

# resolveGroupForGroupType = create1NGetter(GroupModel, foreignKeyName="grouptype_id")

# ## roletype resolvers
# resolveRoleTypeById = createEntityByIdGetter(RoleTypeModel)
# resolveRoleTypeAll = createEntityGetter(RoleTypeModel)
# resolveRoleForRoleType = create1NGetter(RoleModel, foreignKeyName="roletype_id")

# ## role resolvers
# resolverRoleById = createEntityByIdGetter(RoleModel)

# resolveUpdateRole = createUpdateResolver(RoleModel)
# resolveInsertRole = createInsertResolver(RoleModel)


# async def resolveAllRoleTypes(session):
#     stmt = select(RoleTypeModel)
#     dbSet = await session.execute(stmt)
#     result = dbSet.scalars()
#     return result


# def UserByRoleTypeAndGroupStatement(groupId, roleTypeId):
#     stmt = (
#         select(UserModel)
#         .join(RoleModel)
#         .where(RoleModel.group_id == groupId)
#         .where(RoleModel.roletype_id == roleTypeId)
#     )
#     return stmt

# async def resolveUserByRoleTypeAndGroup(session, groupId, roleTypeId):
#     stmt = UserByRoleTypeAndGroupStatement(groupId, roleTypeId)
    
#     dbSet = await session.execute(stmt)
#     result = dbSet.scalars()
#     return result


# from uoishelpers.feeders import ImportModels, ExportModels
# import json
# import datetime


# class ExportEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, uuid.UUID):
#             return f"{obj}"
#         if isinstance(obj, datetime.datetime):
#             return f"{obj}"
#         # Let the base class default method raise the TypeError
#         return json.JSONEncoder.default(self, obj)


# async def export_ug(session):
#     sessionMaker = lambda: session
#     jsonData = await ExportModels(
#         sessionMaker,
#         DBModels=[
#             UserModel,
#             GroupModel,
#             MembershipModel,
#             GroupTypeModel,
#             RoleModel,
#             RoleTypeModel,
#         ],
#     )
#     with open("./extradata/ug_data.json", "w") as f:
#         json.dump(jsonData, f, cls=ExportEncoder)

#     return "ok"


# def datetime_parser(json_dict):
#     for (key, value) in json_dict.items():
#         if key in ["startdate", "enddate"]:
#             dateValue = datetime.datetime.fromisoformat(value)
#             dateValueWOtzinfo = dateValue.replace(tzinfo=None)
#             json_dict[key] = dateValueWOtzinfo
#     return json_dict


# import concurrent.futures
# import asyncio

# from DBDefinitions import ComposeConnectionString, startEngine

# import re


# async def putPredefinedStructuresIntoTable(
#     asyncSessionMaker, DBModel, structureFunction
# ):
#     """Zabezpeci prvotni inicicalizaci zaznamu v databazi
#     DBModel zprostredkovava tabulku,
#     structureFunction() dava data, ktera maji byt ulozena, predpoklada se list of dicts, pricemz dict obsahuje elementarni datove typy
#     """

#     tableName = DBModel.__tablename__
#     # column names
#     cols = [col.name for col in DBModel.metadata.tables[tableName].columns]

#     def mapToCols(item):
#         """z item vybere jen atributy, ktere jsou v DBModel, zbytek je ignorovan"""
#         result = {}
#         for col in cols:
#             value = item.get(col, None)
#             if value is None:
#                 continue
#             result[col] = value
#         return result

#     # ocekavane typy
#     externalIdTypes = structureFunction()

#     # dotaz do databaze
#     stmt = select(DBModel)
#     async with asyncSessionMaker() as session:
#         dbSet = await session.execute(stmt)
#         dbRows = list(dbSet.scalars())

#     # extrakce dat z vysledku dotazu
#     # vezmeme si jen atribut id, id je typu uuid, tak jej zkovertujeme na string
#     idsInDatabase = [f"{row.id}" for row in dbRows]

#     # zjistime, ktera id nejsou v databazi
#     unsavedRows = list(
#         filter(lambda row: not (f'{row["id"]}' in idsInDatabase), externalIdTypes)
#     )

#     async def saveChunk(rows):
#         # pro vsechna neulozena id vytvorime entity
#         # omezime se jen na atributy, ktere jsou definovane v modelu
#         mappedUnsavedRows = list(map(mapToCols, rows))
#         rowsToAdd = [DBModel(**row) for row in mappedUnsavedRows]

#         # a vytvorene entity jednou operaci vlozime do databaze
#         async with asyncSessionMaker() as session:
#             async with session.begin():
#                 session.add_all(rowsToAdd)
#             await session.commit()

#     if len(unsavedRows) > 0:
#         # je co ukladat
#         if "_chunk" in unsavedRows[0]:
#             # existuje informace o rozfazovani ukladani do tabulky
#             nextPhase = [*unsavedRows]
#             while len(nextPhase) > 0:
#                 # zjistime nejmensi cislo poradi ukladani
#                 chunkNumber = min(map(lambda item: item["_chunk"], nextPhase))

#                 print(tableName, "chunkNumber", chunkNumber)

#                 # filtrujeme radky, ktere maji toto cislo
#                 toSave = list(
#                     filter(lambda item: item["_chunk"] == chunkNumber, nextPhase)
#                 )
#                 # ostatni nechame na pozdeji
#                 nextPhase = list(
#                     filter(lambda item: item["_chunk"] != chunkNumber, nextPhase)
#                 )
#                 # ulozime vybrane
#                 await saveChunk(toSave)
#         else:
#             # vsechny zaznamy mohou byt ulozeny soucasne, 
#             # ukladame po blocich
#             while (len(unsavedRows) > 0):
#                 rowsToSave = unsavedRows[:30]
#                 await saveChunk(rowsToSave)
#                 unsavedRows = unsavedRows[30:]

#     # jeste jednou se dotazeme do databaze
#     stmt = select(DBModel)
#     async with asyncSessionMaker() as session:
#         dbSet = await session.execute(stmt)
#         dbRows = dbSet.scalars()

#     # extrakce dat z vysledku dotazu
#     idsInDatabase = [f"{row.id}" for row in dbRows]

#     # znovu zaznamy, ktere dosud ulozeny nejsou, mely by byt ulozeny vsechny, takze prazdny list
#     unsavedRows = list(
#         filter(lambda row: not (f'{row["id"]}' in idsInDatabase), externalIdTypes)
#     )

#     # ted by melo byt pole prazdne
#     if not (len(unsavedRows) == 0):
#         print("SOMETHING is REALLY WRONG")

#     # print(structureFunction(), 'On the input')
#     # print(dbRowsDicts, 'Defined in database')
#     # nyni vsechny entity mame v pameti a v databazi synchronizovane
#     # print(structureFunction())
#     pass

# async def complexDBImport(sessionMaker, jsonData, modelIndex):
#     try:
#         for tableName, DBModel in modelIndex.items():  # iterate over all models
#             # get the appropriate data
#             DBModel.__tablename__ = tableName  # reflexe tento atribut nema :(
#             listData = jsonData.get(tableName, None)
#             if listData is None:
#                 # data does not exists for current model
#                 continue
#             # save data - all rows into a table, if a row with same id exists, do not save it nor update it
#             try:
#                 await putPredefinedStructuresIntoTable(
#                     sessionMaker, DBModel, lambda: listData
#                 )
#             except Exception as e:
#                 print("Exception", e, f"on table {tableName}")

#     except Exception as e:
#         print(e)
    
# async def ImportModels(sessionMaker, DBModels, jsonData):
#     """imports all data from json structure
#     DBModels contains a list of sqlalchemy models
#     jsonData data to import
#     """

#     # create index of all models, key is a table name, value is a model (sqlalchemy model)
#     modelIndex = dict((DBModel.__tablename__, DBModel) for DBModel in DBModels)

#     for tableName, DBModel in modelIndex.items():  # iterate over all models
#         # get the appropriate data

#         listData = jsonData.get(tableName, None)
#         if listData is None:
#             # data does not exists for current model
#             print(f"table {tableName} has no data to import", flush=True)
#             continue

#         print("table", tableName, flush=True)
#         # save data - all rows into a table, if a row with same id exists, do not save it nor update it
#         try:
#             await putPredefinedStructuresIntoTable(
#                 sessionMaker, DBModel, lambda: listData
#             )
#             print(f"table {tableName} import finished", flush=True)
#         except Exception as e:
#             print("Exception", e, f"on table {tableName}")


# # def runImport(sessionMaker, DBModels):
# #     print('runImport Enter', flush=True)
# #     asyncio.run(asyncImport(sessionMaker, DBModels))
# #     print('runImport Leave', flush=True)

# # def runImport2():
# #     print('runImport Enter', flush=True)
# #     try:
# #         newLoop = asyncio.new_event_loop()
# #         newLoop.run_until_complete(asyncImport())
# #         #asyncio.run(asyncImport())
# #     except Exception as e:
# #         print('Error', e, flush=True)
# #     print('runImport Leave', flush=True)


# async def importData(sessionMaker):
#     DBModels = [
#         RoleTypeModel,
#         GroupTypeModel,
#         UserModel,
#         GroupModel,
#         MembershipModel,
#         RoleModel,
#     ]
#     print("asyncImport have DBModels", flush=True)
#     with open("./extradata/ug_data.json", "r") as f:
#         jsonData = json.load(f, object_hook=datetime_parser)
#     print("data in json", flush=True)
#     try:
#         await ImportModels(sessionMaker, DBModels=DBModels, jsonData=jsonData)
#     except Exception as e:
#         print(e)
#     print("*" * 30, flush=True)
#     print("data in DB", flush=True)
#     print("*" * 30, flush=True)


# executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)


# async def import_ug(sessionMaker):

#     # sessionMaker = lambda:session

#     print("import Enter", flush=True)

#     currentLoop = asyncio.get_running_loop()
#     currentLoop.create_task(importData(sessionMaker))

#     # executor.submit(runImport2)
#     # executor.submit(runImport, sessionMaker, [UserModel, GroupModel, MembershipModel, RoleModel, RoleTypeModel, GroupTypeModel])
#     print("import Leave", flush=True)

#     return "ok"


# from strawberry.types.types import TypeDefinition
# from strawberry.utils.inspect import get_func_args
# from graphql import GraphQLObjectType, GraphQLError
# from functools import partial
# from typing import cast, Dict, Any
# import inspect
# import asyncio
# import strawberry


# def create_catch_GraphQLError(get_result, definition):
#     def catch_GraphQLError(representation):
#         try:
#             result = get_result(representation)
#         except Exception as e:
#             result = GraphQLError(
#                 f"Unable to resolve reference for {definition.origin}",
#                 original_error=e,
#             )
#         return result

#     return catch_GraphQLError


# def entities_resolver(self, root, info, representations):
#     results = []
#     type_dict: Dict[str, Dict[str, Any]] = {}
#     for index, representation in enumerate(representations):
#         type_name = representation.pop("__typename")
#         type_ = self.schema_converter.type_map[type_name]
#         type_row = type_dict.get(type_name, None)
#         if type_row is None:
#             type_row = {
#                 "type": type_,
#                 "questions": [],
#                 "indexes": [],
#                 "results": [],
#                 "lazy": False,
#                 "iscoroutinefunction": False,
#                 "get_result": lambda item: None,
#             }
#             type_dict[type_name] = type_row
#             definition = cast(TypeDefinition, type_.definition)
#             key_names = list(representation.keys())
#             if hasattr(definition.origin, "resolve_references") and (
#                 len(key_names) == 1
#             ):
#                 key_name = key_names[0]
#                 type_row["lazy"] = True

#                 resolve_references = definition.origin.resolve_references
#                 type_row["iscoroutinefunction"] = inspect.iscoroutinefunction(
#                     resolve_references
#                 )
#                 func_args = get_func_args(resolve_references)

#                 if key_name not in func_args:

#                     def get_result(
#                         representation,
#                         type_row=type_row,
#                         key_names=key_names,
#                         definition=definition,
#                         resolve_reference=resolve_references,
#                         info=info,
#                         func_args=func_args,
#                     ):
#                         result = (
#                             "Got confused while trying use resolve_references for"
#                             f" {definition.origin}. "
#                             "Resolver resolve_references has not a prameter"
#                             f" {key_names[0]}"
#                         )

#                         raise Exception(result)

#                 else:

#                     def get_result_func(
#                         representation,
#                         type_row=type_row,
#                         key_names=key_names,
#                         definition=definition,
#                         resolve_reference=resolve_references,
#                         info=info,
#                         func_args=func_args,
#                     ):
#                         key_name = key_names[0]
#                         key_values = type_row["questions"]
#                         kwargs = {}
#                         kwargs[key_name] = list(
#                             map(lambda item: item[key_name], key_values)
#                         )
#                         # TODO: use the same logic we use for other resolvers
#                         if "info" in func_args:
#                             kwargs["info"] = info
#                         return resolve_reference(**kwargs)

#                     get_result = create_catch_GraphQLError(get_result_func, definition)
#                 type_row["get_result"] = get_result
#             elif hasattr(definition.origin, "resolve_reference"):
#                 type_row["lazy"] = False

#                 resolve_reference = definition.origin.resolve_reference

#                 func_args = get_func_args(resolve_reference)

#                 # TODO: use the same logic we use for other resolvers
#                 def get_result_func(
#                     representation,
#                     type_row=type_row,
#                     key_names=key_names,
#                     definition=definition,
#                     resolve_reference=resolve_reference,
#                     info=info,
#                     func_args=func_args,
#                 ):
#                     if "info" in func_args:
#                         return resolve_reference(info=info, **representation)
#                     else:
#                         return resolve_reference(**representation)

#                 type_row["get_result"] = create_catch_GraphQLError(
#                     get_result_func, definition
#                 )
#             else:
#                 from strawberry.arguments import convert_argument
#                 from strawberry.type import StrawberryType

#                 type_row["lazy"] = False
#                 strawberry_schema = info.schema.extensions["strawberry-definition"]
#                 config = strawberry_schema.config
#                 scalar_registry = strawberry_schema.schema_converter.scalar_registry

#                 def create_get_result(
#                     convert_argument,
#                     type_par: Union[StrawberryType, type],  # = definition.origin,
#                     scalar_registry_par: Dict[
#                         object, Union[ScalarWrapper, ScalarDefinition]
#                     ],  # = scalar_registry,
#                     config_par: StrawberryConfig,  # = config,
#                 ):
#                     def newfunc(representation_par):
#                         return convert_argument(
#                             representation_par,
#                             type_=type_par,
#                             scalar_registry=scalar_registry_par,
#                             config=config_par,
#                         )

#                     return newfunc

#                 get_result = create_get_result(
#                     convert_argument,
#                     type_pas=definition.origin,
#                     scalar_registry_par=scalar_registry,
#                     config_par=config,
#                 )
#                 type_row["get_result"] = create_catch_GraphQLError(
#                     get_result, definition
#                 )
#         type_row["indexes"].append(index)
#         type_row["questions"].append(representation)

#     async def awaitable_wrapper(index, row):
#         semaphore = row["semaphore"]
#         list_of_indexes = row["indexes"]
#         index_of = list_of_indexes.index(index)
#         async with semaphore:
#             list_of_results = row["results"]
#             if inspect.isawaitable(list_of_results):
#                 list_of_results = await list_of_results
#                 row["results"] = list_of_results
#             single_result = list_of_results[index_of]
#         return single_result

#     def sync_wrapper(index, row):
#         list_of_indexes = row["indexes"]
#         list_of_results = row["results"]
#         index_of = list_of_indexes.index(index)
#         single_result = list_of_results[index_of]
#         return single_result

#     indexed_results = []
#     for _entity_name, row in type_dict.items():
#         if row["lazy"]:
#             get_result = row["get_result"]
#             result = get_result(None)
#             row["results"] = result
#             if type_row["iscoroutinefunction"]:
#                 row["semaphore"] = asyncio.BoundedSemaphore(1)
#                 current_indexed_results = [
#                     (index, awaitable_wrapper(index, row)) for index in row["indexes"]
#                 ]
#             else:
#                 current_indexed_results = [
#                     (index, sync_wrapper(index, row)) for index in row["indexes"]
#                 ]
#             indexed_results.extend(current_indexed_results)
#         else:
#             get_result = row["get_result"]
#             row["results"] = [get_result(item) for item in row["questions"]]
#             current_indexed_results = [
#                 (index, result) for index, result in zip(row["indexes"], row["results"])
#             ]
#             indexed_results.extend(current_indexed_results)

#     indexed_results.sort(key=lambda a: a[0])
#     results = list(map(lambda item: item[1], indexed_results))
#     return results

import strawberry
import uuid
import datetime
import typing
import logging

from .BaseGQLModel import IDType

UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".externals")]
GroupGQLModel = typing.Annotated["GroupGQLModel", strawberry.lazy(".externals")]

@strawberry.field(description="""Entity primary key""")
def resolve_id(self) -> IDType:
    return self.id

@strawberry.field(description="""Name """)
def resolve_name(self) -> str:
    return self.name

@strawberry.field(description="""English name""")
def resolve_name_en(self) -> str:
    result = self.name_en if self.name_en else ""
    return result

@strawberry.field(description="""Time of last update""")
def resolve_lastchange(self) -> datetime.datetime:
    return self.lastchange

@strawberry.field(description="""Time of entity introduction""")
def resolve_created(self) -> typing.Optional[datetime.datetime]:
    return self.created

async def resolve_user(user_id):
    from GraphTypeDefinitions import UserGQLModel
    result = None if user_id is None else await UserGQLModel.resolve_reference(user_id)
    return result
    
@strawberry.field(description="""Who created entity""")
async def resolve_createdby(self) -> typing.Optional["UserGQLModel"]:
    return await resolve_user(self.createdby)

@strawberry.field(description="""Who made last change""")
async def resolve_changedby(self) -> typing.Optional["UserGQLModel"]:
    return await resolve_user(self.changedby)

RBACObjectGQLModel = typing.Annotated["RBACObjectGQLModel", strawberry.lazy(".externals")]
@strawberry.field(description="""Who made last change""")
async def resolve_rbacobject(self, info: strawberry.types.Info) -> typing.Optional[RBACObjectGQLModel]:
    from GraphTypeDefinitions import RBACObjectGQLModel
    result = None if self.rbacobject is None else await RBACObjectGQLModel.resolve_reference(info, self.rbacobject)
    return result

resolve_result_id: IDType = strawberry.field(description="primary key of CU operation object")
resolve_result_msg: str = strawberry.field(description="""Should be `ok` if descired state has been reached, otherwise `fail`.
For update operation fail should be also stated when bad lastchange has been entered.""")

from inspect import signature
import inspect 
from functools import wraps

def asPage(field, *, extendedfilter=None):
    def decorator(field):
        print(field.__name__, field.__annotations__)
        signatureField = signature(field)
        return_annotation = signatureField.return_annotation

        skipParameter = signatureField.parameters.get("skip", None)
        skipParameterDefault = 0
        if skipParameter:
            skipParameterDefault = skipParameter.default

        limitParameter = signatureField.parameters.get("limit", None)
        limitParameterDefault = 10
        if limitParameter:
            limitParameterDefault = limitParameter.default

        whereParameter = signatureField.parameters.get("where", None)
        whereParameterDefault = None
        whereParameterAnnotation = str
        if whereParameter:
            whereParameterDefault = whereParameter.default
            whereParameterAnnotation = whereParameter.annotation

        async def foreignkeyVectorSimple(
            self, info: strawberry.types.Info,
            skip: typing.Optional[int] = skipParameterDefault,
            limit: typing.Optional[int] = limitParameterDefault
        ) -> signature(field).return_annotation:
            loader = await field(self, info)
            results = await loader.page(skip=skip, limit=limit, extendedfilter=extendedfilter)
            return results
        foreignkeyVectorSimple.__name__ = field.__name__
        foreignkeyVectorSimple.__doc__ = field.__doc__

        async def foreignkeyVectorComplex(
            self, info: strawberry.types.Info, 
            where: whereParameterAnnotation = None, 
            #where: typing.Optional[whereParameterAnnotation] = whereParameterDefault, 
            #where: typing.Optional[str] = None, 
            orderby: typing.Optional[str] = None, 
            desc: typing.Optional[bool] = None, 
            skip: typing.Optional[int] = skipParameterDefault,
            limit: typing.Optional[int] = limitParameterDefault
        ) -> signatureField.return_annotation:
            # logging.info(f"waiting for a loader {where}")
            wf = None if where is None else strawberry.asdict(where)
            loader = await field(self, info, where=wf)    
            # logging.info(f"got a loader {loader}")
            # wf = None if where is None else strawberry.asdict(where)
            results = await loader.page(skip=skip, limit=limit, where=wf, orderby=orderby, desc=desc, extendedfilter=extendedfilter)
            return results
        foreignkeyVectorComplex.__name__ = field.__name__
        foreignkeyVectorComplex.__doc__ = field.__doc__
        
        if return_annotation._name == "List":
            return foreignkeyVectorComplex if whereParameter else foreignkeyVectorSimple
        else:
            raise Exception("Unable to recognize decorated function, I am sorry")

    return decorator(field) if field else decorator

def asForeignList(*, foreignKeyName: str):
    assert foreignKeyName is not None, "foreignKeyName must be defined"
    def decorator(field):
        print(field.__name__, field.__annotations__)
        signatureField = signature(field)
        return_annotation = signatureField.return_annotation

        skipParameter = signatureField.parameters.get("skip", None)
        skipParameterDefault = skipParameter.default if skipParameter else 0

        limitParameter = signatureField.parameters.get("limit", None)
        limitParameterDefault = limitParameter.default if limitParameter else 10

        whereParameter = signatureField.parameters.get("where", None)
        whereParameterDefault = whereParameter.default if whereParameter else None
        whereParameterAnnotation = whereParameter.annotation if whereParameter else str

        async def foreignkeyVectorSimple(
            self, info: strawberry.types.Info,
            skip: typing.Optional[int] = skipParameterDefault,
            limit: typing.Optional[int] = limitParameterDefault
        ) -> signature(field).return_annotation:
            extendedfilter = {}
            extendedfilter[foreignKeyName] = self.id
            loader = field(self, info)
            if inspect.isawaitable(loader):
                loader = await loader
            results = await loader.page(skip=skip, limit=limit, extendedfilter=extendedfilter)
            return results
        foreignkeyVectorSimple.__name__ = field.__name__
        foreignkeyVectorSimple.__doc__ = field.__doc__
        foreignkeyVectorSimple.__module__ = field.__module__

        async def foreignkeyVectorComplex(
            self, info: strawberry.types.Info, 
            where: whereParameterAnnotation = whereParameterDefault, 
            orderby: typing.Optional[str] = None, 
            desc: typing.Optional[bool] = None, 
            skip: typing.Optional[int] = skipParameterDefault,
            limit: typing.Optional[int] = limitParameterDefault
        ) -> signatureField.return_annotation:
            extendedfilter = {}
            extendedfilter[foreignKeyName] = self.id
            loader = field(self, info)
            if inspect.isawaitable(loader):
                loader = await loader
            
            wf = None if where is None else strawberry.asdict(where)
            results = await loader.page(skip=skip, limit=limit, where=wf, orderby=orderby, desc=desc, extendedfilter=extendedfilter)
            return results
        foreignkeyVectorComplex.__name__ = field.__name__
        foreignkeyVectorComplex.__doc__ = field.__doc__
        foreignkeyVectorComplex.__module__ = field.__module__

        async def foreignkeyVectorComplex2(
            self, info: strawberry.types.Info, 
            where: whereParameterAnnotation = whereParameterDefault, 
            orderby: typing.Optional[str] = None, 
            desc: typing.Optional[bool] = None, 
            skip: typing.Optional[int] = skipParameterDefault,
            limit: typing.Optional[int] = limitParameterDefault
        ) -> signatureField.return_annotation: #typing.List[str]:
            extendedfilter = {}
            extendedfilter[foreignKeyName] = self.id
            loader = field(self, info)
            
            wf = None if where is None else strawberry.asdict(where)
            results = await loader.page(skip=skip, limit=limit, where=wf, orderby=orderby, desc=desc, extendedfilter=extendedfilter)
            return results
        foreignkeyVectorComplex2.__module__ = field.__module__
        if return_annotation._name == "List":
            return foreignkeyVectorComplex if whereParameter else foreignkeyVectorSimple
        else:
            raise Exception("Unable to recognize decorated function, I am sorry")

    return decorator
# def createAttributeScalarResolver(

# def createAttributeScalarResolver(
#     scalarType: None = None, 
#     foreignKeyName: str = None,
#     description="Retrieves item by its id",
#     permission_classes=()
#     ):

#     assert scalarType is not None
#     assert foreignKeyName is not None

#     @strawberry.field(description=description, permission_classes=permission_classes)
#     async def foreignkeyScalar(
#         self, info: strawberry.types.Info
#     ) -> typing.Optional[scalarType]:
#         # 👇 self must have an attribute, otherwise it is fail of definition
#         assert hasattr(self, foreignKeyName)
#         id = getattr(self, foreignKeyName, None)
        
#         result = None if id is None else await scalarType.resolve_reference(info=info, id=id)
#         return result
#     return foreignkeyScalar

# def createAttributeVectorResolver(
#     scalarType: None = None, 
#     whereFilterType: None = None,
#     foreignKeyName: str = None,
#     loaderLambda = lambda info: None, 
#     description="Retrieves items paged", 
#     skip: int=0, 
#     limit: int=10):

#     assert scalarType is not None
#     assert foreignKeyName is not None

#     @strawberry.field(description=description)
#     async def foreignkeyVector(
#         self, info: strawberry.types.Info,
#         skip: int = skip,
#         limit: int = limit,
#         where: typing.Optional[whereFilterType] = None
#     ) -> typing.List[scalarType]:
        
#         params = {foreignKeyName: self.id}
#         loader = loaderLambda(info)
#         assert loader is not None
        
#         wf = None if where is None else strawberry.asdict(where)
#         result = await loader.page(skip=skip, limit=limit, where=wf, extendedfilter=params)
#         return result
#     return foreignkeyVector

def createRootResolver_by_id(scalarType: None, description="Retrieves item by its id"):
    assert scalarType is not None
    @strawberry.field(description=description)
    async def by_id(
        self, info: strawberry.types.Info, id: IDType
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
    order_by: typing.Optional[str] = None,
    desc: typing.Optional[bool] = None):

    assert scalarType is not None
    assert whereFilterType is not None
    
    @strawberry.field(description=description)
    async def paged(
        self, info: strawberry.types.Info, 
        skip: int=skip, limit: int=limit, where: typing.Optional[whereFilterType] = None
    ) -> typing.List[scalarType]:
        loader = loaderLambda(info)
        assert loader is not None
        wf = None if where is None else strawberry.asdict(where)
        result = await loader.page(skip=skip, limit=limit, where=wf, orderby=order_by, desc=desc)
        return result
    return paged
