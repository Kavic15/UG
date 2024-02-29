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

test_reference_roleType = createResolveReferenceTest(
    tableName='roletypes', gqltype='RoleTypeGQLModel', 
    attributeNames=["id"])
test_query_roleType_by_id = createByIdTest(tableName="roletypes", queryEndpoint="roleTypeById")
test_query_roleType_page = createPageTest(tableName="roletypes", queryEndpoint="roleTypePage")

test_roleType_insert = createFrontendQuery(query="""
     mutation($name: String!,  $nameEn: String!, $categoryId: UUID!) { 
        result: roleTypeInsert(roletype: {name: $name, nameEn: $nameEn, categoryId: $categoryId}) { 
            id
            msg
            roleType {
                id
                name
                nameEn
                lastchange
                created                 
                changedby { id }            
            }
        }
    }
    """, 
    variables={
        "categoryId": "fd73596b-1043-46f0-837a-baa0734d64df",
        "name": "nepreziju_to",
        "nameEn": "kys"
    },
    asserts=[]
)

test_roleType_update = createUpdateQuery(
    query="""
       mutation ($id: UUID!, $name: String!, $lastchange: DateTime!) {
        result: roleTypeUpdate(
            roletype: {id: $id, name: $name, lastchange: $lastchange}
        ) {
            id
            msg
            roleType {
                id
                lastchange
                }
            }
        }
    """,
    variables={  "id": "05a3e0f5-f71e-4caa-8012-229d868aa8ca",
                "name": "nepreziju_to",
            },
    tableName="roletypes"
)

#TODO
test_roleType_delete = createDeleteQuery(tableName="roletypes", queryBase="roletype", attributeNames=["id"], id="ced46aa4-3217-4fc1-b79d-f6be7d21c6b6")