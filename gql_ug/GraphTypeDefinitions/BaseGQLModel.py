import strawberry
import uuid
import datetime
import typing

class BaseGQLModel:
    @classmethod
    # def getLoader(cls, info):
    #     pass

    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: uuid.UUID ):
        if id is not None:
            return None
        loader = cls.getLoader(info)
        if isinstance(id, str): id = uuid.UUID(id)
        result = await loader.load(id)
        if result is not None:
            result.__strawberry_definition__ = cls.__strawberry_definition__  # little hack :)
        return result

