import strawberry
import uuid
import datetime
import typing

class BaseGQLModel:
    @classmethod
    def getLoader(cls, info):
        pass

    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        if id is None: return None
        loader = cls.getLoader(info)
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
            result.__strawberry_definition__ = cls._type_definition # some version of strawberry changed :(
        return result

