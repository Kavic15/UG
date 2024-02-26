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

test_reference_roleCategory = createResolveReferenceTest(
    tableName='rolecategories', gqltype='roleCategoryGQLModel', 
    attributeNames=["id", "name", "nameEn", "lastchange", "creator {id}", "createdby {id}"])
test_query_roleCategory_by_id = createByIdTest(tableName="rolecategories", queryEndpoint="roleCategoryById")
test_query_roleCategory_page = createPageTest(tableName="rolecategories", queryEndpoint="roleCategoryPage")

test_roleCategory_insert = createFrontendQuery(query="""
    mutation($id: UUID!, $name: String!, $nameEn: String!, $rbac_id: UUID!) { 
        result: roleCategoryInsert(roleCategory: {id: $id, name: $name, nameEn: $nameEn, rbacobject: $rbac_id}) { 
            id
            msg
            roleCategory {
                id
                name
                nameEn
                lastchange
                created
                                       
                changedby { id }
                rbacobject { id }                
            }
        }
    }
    """, 
    variables={"id": "ccde3a8b-81d0-4e2b-9aac-42e0ea2255b3", "name": "new roleCategory", "nameEn": "new roleCategory", "rbac_id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003"},
    asserts=[]
)

test_roleCategory_update = createUpdateQuery(
    query="""
        mutation($id: UUID!, $name: String!, $nameEn: String!, $lastchange: DateTime!) {
            roleCategoryUpdate(roleCategory: {id: $id, name: $name, nameEn: $nameEn, lastchange: $lastchange}) {
                result: roleCategoryInsert(roleCategory: {id: $id, name: $name, nameEn: $nameEn, rbacobject: $rbac_id}) { 
                    id
                    msg
                    roleCategory {
                        id
                        name
                        nameEn
                        lastchange
                        created
                                            
                        changedby { id }
                        rbacobject { id }
                    }
                }
            }
        }
    """,
    variables={"id": "191d578c-afb1-11ed-9bd8-0242ac110002", "name": "new name", "nameEn": "new nameEn"},
    tableName="rolecategories"
)