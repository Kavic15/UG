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

test_reference_role = createResolveReferenceTest(
    tableName='roles', gqltype='RoleGQLModel', 
    attributeNames=["id"])
# nemáš xD, musis udelat 
test_query_role_by_id = createByIdTest(tableName="roles", queryEndpoint="roleById")
test_query_role_page = createPageTest(tableName="roles", queryEndpoint="rolePage")

test_role_insert = createFrontendQuery(query="""
   mutation($user_id: UUID!, $group_id: UUID!,$roletype_id: UUID!) {
        result: roleInsert(role: {userId: $user_id, groupId: $group_id, roletypeId: $roletype_id}) {
            id
            msg
            role {
                id                      
                lastchange
                valid 
                changedby { id }
                group { id }
            }
        }
    }
    """, 
    variables={
        "user_id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
        "group_id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
        "roletype_id": "ced46aa4-3217-4fc1-b79d-f6be7d21c6b6"
        },
    asserts=[]
)

test_role_update = createUpdateQuery(
    query="""
        mutation ($id: UUID!, $name: String!, $lastchange: DateTime!, $roletypeId: UUID!) {
            result: roleUpdate(
                role: {id: $id, name: $name, lastchange: $lastchange, roletypeId: $roletypeId}
            ) {
                id
                msg
                role {
                    id
                    lastchange
                }
            }
        }
    """,
    variables={  "id": "2d9dc5ca-a4a2-11ed-b9df-0242ac125003",
                "name": "nepreziju_to",
                "roletypeId": "ced46aa4-3217-4fc1-b79d-f6be7d21c6b6"
               },
    tableName="roles"
)

#TODO
test_role_delete = createDeleteQuery(tableName="roles", queryBase="role", attributeNames=["id"], id="2d9dc5ca-a4a2-11ed-b9df-0242ac125003")