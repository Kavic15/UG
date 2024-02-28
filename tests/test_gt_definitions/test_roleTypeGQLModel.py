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

test_reference_roleType = createResolveReferenceTest(
    tableName='roletypes', gqltype='RoleTypeGQLModel', 
    attributeNames=["id", "name", "nameEn", "lastchange", "category_id", "creator {id}", "createdby {id}"])
test_query_roleType_by_id = createByIdTest(tableName="roletypes", queryEndpoint="roleTypeById")
test_query_roleType_page = createPageTest(tableName="roletypes", queryEndpoint="roleTypePage")

test_roleType_insert = createFrontendQuery(query="""
    mutation($id: UUID!, $name: String!,  $nameEn: String!, $rbac_id: UUID!) { 
        result: roleTypeInsert(roletype: {id: $id, name: $name, nameEn: $nameEn, rbacobject: $rbac_id}) { 
            id
            msg
            roletype {
                id
                name
                nameEn
                category_id
                lastchange
                created
                                       
                changedby { id }
                rbacobject { id }                
            }
        }
    }
    """, 
    variables={"id": "ccde3a8b-81d0-4e2b-9aac-42e0eb2255b3", "name": "new roletype", "rbac_id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003"},
    asserts=[]
)

test_roleType_update = createUpdateQuery(
    query="""
        mutation($id: UUID!, $name: String!, $lastchange: DateTime!) {
            roleTypeUpdate(roletype: {id: $id, name: $name, lastchange: $lastchange}) {
                result: roleTypeInsert(roletype: {id: $id, name: $name, nameEn: $nameEn, rbacobject: $rbac_id}) { 
                    id
                    msg
                    roletype {
                        id
                        name
                        nameEn
                        category_id
                        lastchange
                        created
                                            
                        changedby { id }
                        rbacobject { id }                
                    }
                }
            }
        }
    """,
    variables={"id": "190d578c-afb1-11ed-9bd8-0242ac110002", "name": "new name", "nameEn": "new nameEn"},
    tableName="roletypes"
)
