import strawberry

@strawberry.type(description="""Type for query root""")
class Query:

    from .groupGQLModel import group_by_id
    group_by_id = group_by_id

    from .groupGQLModel import group_page
    group_page = group_page

    from .groupGQLModel import group_by_letters
    group_by_letters = group_by_letters