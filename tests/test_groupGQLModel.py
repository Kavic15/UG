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

test_reference_group = createResolveReferenceTest(tableName='groups', gqltype='GroupGQLModel')
test_query_group_by_id = createByIdTest(tableName="groups", queryEndpoint="groupById")
test_query_group_page = createPageTest(tableName="groups", queryEndpoint="groupPage")

test_group_insert = createFrontendQuery(
    query="""
        mutation($id: UUID!, $name: String!, $grouptype_id: UUID!) {
            result: groupInsert(group: {id: $id, name: $name, grouptypeId: $grouptype_id}) {
                id
                msg
                group {
                    name
                    lastchange
                    created
                    valid
                                        
                    rbacobject { id }
                }
            }
        }
    """, 
    variables={"id": "d6b88d4b-deba-4ddc-bb66-4dd892e33772", "name": "new group", "grouptype_id": "cd49e152-610c-11ed-9f29-001a7dda7110"},
    asserts=[]
)

test_group_update = createUpdateQuery(
    query="""
        mutation($id: UUID!, $name: String!, $lastchange: DateTime!) {
            result: groupUpdate(group: {id: $id, name: $name, lastchange: $lastchange}) {
                id
                group {
                    name
                    lastchange
                }
            }
        }""",
    variables={"id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003", "name": "new name"},
    tableName="groups"
)

