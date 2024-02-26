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

from tests.gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

test_reference_role = createResolveReferenceTest(
    tableName='roles', gqltype='RoleGQLModel', 
    attributeNames=["id", "user_id", "group_id", "roletype_id", "lastchange", "startdate", "enddate", "valid", "creator {id}", "createdby {id}"])
test_query_role_by_id = createByIdTest(tableName="roles", queryEndpoint="roleById")
test_query_role_page = createPageTest(tableName="roles", queryEndpoint="rolePage")

test_role_insert = createFrontendQuery(query="""
    mutation($id: UUID!, $user_id: UUID!, $group_id: UUID!,$roletype_id: UUID!, $rbac_id: UUID!) {
        result: roleInsert(role: {id: $id, user_id: $user_id, group_id: $group_id, roletype_id: $roletype_id, rbacobject: $rbac_id}) {
            id
            msg
            role {
                id
                user_id
                group_id                
                roletype_id
                lastchange
                startdate
                enddate
                created
                valid
                                       
                changedby { id }
                rbacobject { id }
            }
        }
    }
    """, 
    variables={"id": "ccde3a8b-81d0-4e2b-9aac-42e0eb2255b3", "name": "new role", "rbac_id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003"},
    asserts=[]
)

test_role_update = createUpdateQuery(
    query="""
        mutation($id: UUID!, $name: String!, $lastchange: DateTime!) {
            roleUpdate(role: {id: $id, name: $name, lastchange: $lastchange}) {
                result: roleInsert(role: {id: $id, user_id: $user_id, group_id: $group_id, roletype_id: $roletype_id, rbacobject: $rbac_id}) {
                    id
                    msg
                    role {
                        id
                        user_id
                        group_id                
                        roletype_id
                        lastchange
                        startdate
                        enddate
                        created
                        valid
                                            
                        changedby { id }
                        rbacobject { id }
                    }
                }
            }
        }
    """,
    variables={"id": "190d578c-afb1-11ed-9bd8-0242ac110002",
               "user_id": "4fad9a3d-6c34-4f6f-915d-ad7f50ec85d5",
               "group_id": "4fbd9a3d-6c34-4f6f-915d-ad7f50ec85d5",
               "roletype_id": "4fad9a3d-6c34-4f6f-915a-ad7f50ec85d5",},
    tableName="roles"
)