import strawberry

@strawberry.type
class Mutation:
    from .groupGQLModel import group_insert
    group_insert = group_insert

    from .groupGQLModel import group_update
    group_update = group_update

    from .groupGQLModel import group_delete
    group_delete = group_delete