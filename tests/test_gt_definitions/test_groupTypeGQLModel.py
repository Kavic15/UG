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

test_reference_groupType = createResolveReferenceTest(tableName='grouptypes', gqltype='GroupTypeGQLModel')
test_query_groupType_by_id = createByIdTest(tableName="grouptypes", queryEndpoint="groupTypeById")
test_query_groupType_page = createPageTest(tableName="grouptypes", queryEndpoint="groupTypePage")

test_groupType_insert = createFrontendQuery(query="""
    mutation($id: UUID!, $name: String!) { 
        result: groupTypeInsert(grouptype: {id: $id, name: $name}) { 
            id
            msg
            grouptype {
                id
                name
                lastchange
                created
                valid
                                       
                groups { id }
            }
        }
    }
    """, 
    variables={"id": "ccde3a8b-81d0-4e2b-9aac-42e0eb2255b3", "name": "new grouptype"},
    asserts=[]
)

test_groupType_update = createUpdateQuery(
    query="""
        mutation($id: UUID!, $name: String!, $lastchange: DateTime!) {
            groupTypeUpdate(grouptype: {id: $id, name: $name, lastchange: $lastchange}) {
                result: groupTypeInsert(grouptype: {id: $id, name: $name}) { 
                    id
                    msg
                    grouptype {
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
    variables={"id": "190d578c-afb1-11ed-9bd8-0243ac110002", "name": "new name"},
    tableName="groupTypes"
)