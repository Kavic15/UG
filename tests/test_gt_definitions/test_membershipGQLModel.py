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

test_reference_membership = createResolveReferenceTest(
    tableName='memberships', gqltype='MembershipGQLModel', 
    attributeNames=["id"])
test_query_membership_by_id = createByIdTest(tableName="memberships", queryEndpoint="membershipById", attributeNames=["id"])
test_query_membership_page = createPageTest(tableName="memberships", queryEndpoint="membershipPage", attributeNames=["id"])

test_membership_insert = createFrontendQuery(query="""
    mutation ($userId: UUID!, $groupId: UUID!) {
        result: membershipInsert(membership: {userId: $userId, groupId: $groupId}) {
            id
            msg
            membership {
                id
                lastchange
                created
                valid
                user {
                    id
                }
                group {
                    id
                }
                changedby {
                    id
                }
            }
        }
    }
    """, 
    variables={
  "userId": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
  "groupId": "2d9dcd22-a4a2-11ed-b9df-0242ac120003"
        },
    asserts=[]
)

test_membership_update = createUpdateQuery(
    query="""
        mutation ($id: UUID!, $lastchange: DateTime!) {
            result: membershipUpdate(
                membership: {id: $id, lastchange: $lastchange}
            ) {
                id
                msg
                membership {
                    id
                    lastchange
                }
            }
        }
    """,
    variables={
          "id": "7cea8596-a4a2-11ed-b9df-0242ac120003"
    },
    tableName="memberships"
)

test_membership_delete = createDeleteQuery(tableName="memberships", queryBase="membership", attributeNames=["id"], id="7cea8596-a4a2-11ed-b9df-0242ac120003")

