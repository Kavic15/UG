import pytest
# import os
# os.environ["GQLUG_ENDPOINT_URL"] = "http://localhost:8124/gql"
# print(os.environ.get("GQLUG_ENDPOINT_URL", None))


# from ..gqlshared import (
#     createByIdTest, 
#     createPageTest, 
#     createResolveReferenceTest, 
#     createFrontendQuery, 
#     createUpdateQuery
# )

from gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery,
    createDeleteQuery
)

test_reference_user = createResolveReferenceTest(
    tableName='users', gqltype='UserGQLModel', 
    attributeNames=["id"])
test_query_user_by_id = createByIdTest(tableName="users", queryEndpoint="userById")
test_query_user_page = createPageTest(tableName="users", queryEndpoint="userPage")

test_user_insert = createFrontendQuery(
    query="""
        mutation ($name: String!, $surname: String!) {
            result: userInsert(
                user: {name: $name, surname: $surname}
            ) {
                id
                msg
                user {
                    id
                    name
                    surname
                    email
                    lastchange
                    created
                    valid
                    changedby {
                        id
                        surname
                        email
                    }
                    membership {
                        id
                    }
                    roles {
                        id
                    }
                    memberOf(grouptypeId: "cd49e152-610c-11ed-9f29-001a7dda7110") {
                        id
                    }
                }
            }
        }
    """, 
    variables={  
        "surname": "sikovny",
        "name": "kluk"
        },
    asserts=[]
)

test_user_update = createUpdateQuery(
    query="""
    mutation ($id: UUID!, $name: String!, $lastchange: DateTime!) {
        result: userUpdate(user: {id: $id, name: $name, lastchange: $lastchange}) {
            id
            msg
            user {
                id
                lastchange
                }
        }
    }
    """,
    variables={  
        "lastchange": "2024-02-28T22:26:42.076425",
        "name": "kluk",
        "id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003"},
    tableName="users"
)

#TODO
test_user_delete = createDeleteQuery(tableName="users", queryBase="user", attributeNames=["id"], id="89d1f534-ae0f-11ed-9bd8-0242ac110002")
