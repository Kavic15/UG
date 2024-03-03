import strawberry

@strawberry.type(description="""Type for query root""")
class Query:

    from .userGQLModel import user_by_id
    user_by_id = user_by_id

    from .userGQLModel import user_page
    user_page = user_page

    from .groupGQLModel import group_by_id
    group_by_id = group_by_id

    from .groupGQLModel import group_page
    group_page = group_page

    from .roleTypeGQLModel import role_type_by_id
    role_type_by_id = role_type_by_id

    from .roleTypeGQLModel import role_type_page
    role_type_page = role_type_page

    from .roleCategoryGQLModel import role_category_by_id
    role_category_by_id = role_category_by_id

    from .roleCategoryGQLModel import role_category_page
    role_category_page = role_category_page

    from .groupTypeGQLModel import group_type_by_id
    group_type_by_id = group_type_by_id

    from .groupTypeGQLModel import group_type_page
    group_type_page = group_type_page
    
    from .membershipGQLModel import membership_page
    membership_page = membership_page

    from .membershipGQLModel import membership_by_id
    membership_by_id = membership_by_id

    from .roleGQLModel import role_by_user
    role_by_user = role_by_user

    from .roleGQLModel import roles_on_group
    roles_on_group = roles_on_group

    from .roleGQLModel import roles_on_user
    roles_on_user = roles_on_user

    from .roleGQLModel import role_page
    role_page = role_page

    from .roleGQLModel import role_by_id
    role_by_id = role_by_id

    from .RBACObjectGQLModel import rbac_by_id
    rbac_by_id = rbac_by_id
