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

from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

test_reference_user = createResolveReferenceTest(
    tableName='users', gqltype='UserGQLModel', 
    attributeNames=["id", "name", "surname", "email", "lastchange", "valid", "creator {id}", "createdby {id}"])
test_query_user_by_id = createByIdTest(tableName="users", queryEndpoint="userById")
test_query_user_page = createPageTest(tableName="users", queryEndpoint="userPage")

test_user_insert = createFrontendQuery(query="""
    mutation($id: UUID!, $name: String!, $rbac_id: UUID!) { 
        result: userInsert(user: {id: $id, name: $name, surname: $surname, rbacobject: $rbac_id}) { 
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
                                       
                changedby { id }
                rbacobject { id }                
            }
        }
    }
    """, 
    variables={"id": "ccde3a8b-81d0-4e2b-9aac-42e0eb2255b3", "name": "new user", "rbac_id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003"},
    asserts=[]
)

test_user_update = createUpdateQuery(
    query="""
        mutation($id: UUID!, $name: String!, $lastchange: DateTime!) {
            userUpdate(user: {id: $id, name: $name, lastchange: $lastchange}) {
                result: userInsert(user: {id: $id, name: $name, surname: $surname, rbacobject: $rbac_id}) { 
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

                        changedby { id }
                    }
                }
            }
        }
    """,
    variables={"id": "190d578c-afb1-11ed-9bd8-0242ac110002", "name": "new name"},
    tableName="users"
)
