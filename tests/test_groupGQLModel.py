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
    createUpdateQuery,
)

test_reference_group = createResolveReferenceTest(
    tableName='groups', gqltype='GroupGQLModel', 
    attributeNames=["id", "name", "lastchange", "valid", "creator {id}", "createdby {id}"])
test_query_group_by_id = createByIdTest(tableName="groups", queryEndpoint="groupById")
test_query_group_page = createPageTest(tableName="groups", queryEndpoint="groupPage")

test_group_insert = createFrontendQuery(query="""
    mutation($id: UUID!, $name: String!, $rbac_id: UUID!) { 
        result: groupInsert(group: {id: $id, name: $name, surname: $surname, rbacobject: $rbac_id}) { 
            id
            msg
            group {
                id
                name
                lastchange
                created
                valid
                                       
                changedby { id }         
            }
        }
    }
    """, 
    variables={"id": "ccde3a8b-81d0-4e2b-9aac-42e0eb2255b3", "name": "new group", "rbac_id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003"},
    asserts=[]
)

test_group_update = createUpdateQuery(
    query="""
        mutation($id: UUID!, $name: String!, $lastchange: DateTime!) {
            groupUpdate(group: {id: $id, name: $name, lastchange: $lastchange}) {
                result: groupInsert(group: {id: $id, name: $name, surname: $surname, rbacobject: $rbac_id}) { 
                    id
                    msg
                    group {
                        id
                        name
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
    tableName="groups"
)

