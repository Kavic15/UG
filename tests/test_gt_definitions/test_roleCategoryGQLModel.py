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

test_reference_roleCategory = createResolveReferenceTest(
    tableName='rolecategories', gqltype='RoleCategoryGQLModel', 
    attributeNames=["id"])
test_query_roleCategory_by_id = createByIdTest(tableName="rolecategories", queryEndpoint="roleCategoryById")
test_query_roleCategory_page = createPageTest(tableName="rolecategories", queryEndpoint="roleCategoryPage")

test_roleCategory_insert = createFrontendQuery(query="""
    mutation($name: String!, $nameEn: String!) { 
        result: roleCategoryInsert(rolecategory: {name: $name, nameEn: $nameEn}) { 
            id
            msg
            roleCategory {
                id
                name
                nameEn
                lastchange
                created
                roleTypes { id }
                rbacobject { id }
                changedby { id }            
            }
        }
    }
    """, 
    variables={"name": "new rolecategory", "nameEn": "new rolecategory"},
    asserts=[]
)

test_roleCategory_update = createUpdateQuery(
    query="""
        mutation($id: UUID!, $lastchange: DateTime!, $name: String) 
        {
            result: roleCategoryUpdate(rolecategory: {id: $id, lastchange: $lastchange, name: $name}) 
            { 
                id
                msg
                roleCategory {
                    id
                    name
                    lastchange
                }
            }
        }
    """,
    variables={
        "id": "fd73596b-1043-46f0-837a-baa0734d64df",
        "name": "new name1"
    },
    tableName="rolecategories"
)

#TODO
test_roleCategory_delete = createDeleteQuery(tableName="rolecategories", queryBase="roleCategory", attributeNames=["id"], id="fd73596b-1043-46f0-837a-baa0734d64df")