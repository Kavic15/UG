import strawberry

@strawberry.type
class Mutation:
    from .groupGQLModel import group_insert
    group_insert = group_insert

    from .groupGQLModel import group_update
    group_update = group_update

    from .groupGQLModel import group_delete
    group_delete = group_delete

    from .userGQLModel import user_insert
    user_insert = user_insert

    from .userGQLModel import user_update
    user_update = user_update

    from .userGQLModel import user_delete
    user_delete = user_delete

    from .membershipGQLModel import membership_insert
    membership_insert = membership_insert

    from .membershipGQLModel import membership_update
    membership_update = membership_update

    from .roleGQLModel import role_insert
    role_insert = role_insert

    from .roleGQLModel import role_update
    role_update = role_update

    from .roleGQLModel import role_delete
    role_delete = role_delete

    from .roleTypeGQLModel import role_type_insert
    role_type_insert = role_type_insert

    from .roleTypeGQLModel import role_type_update
    role_type_update = role_type_update

    from .roleTypeGQLModel import role_type_delete
    role_type_delete = role_type_delete

    from .roleCategoryGQLModel import role_category_insert
    role_category_insert = role_category_insert

    from .roleCategoryGQLModel import role_category_update
    role_category_update = role_category_update

    from .roleCategoryGQLModel import role_category_delete
    role_category_delete = role_category_delete

    from .groupTypeGQLModel import group_type_insert
    group_type_insert = group_type_insert

    from .groupTypeGQLModel import group_type_update
    group_type_update = group_type_update

    from .groupTypeGQLModel import group_type_delete
    group_type_delete = group_type_delete
