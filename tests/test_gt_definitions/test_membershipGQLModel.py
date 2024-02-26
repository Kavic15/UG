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

test_reference_membership = createResolveReferenceTest(
    tableName='memberships', gqltype='MembershipGQLModel', 
    attributeNames=["id", "membership_id", "group_id", "lastchange", "valid", "creator {id}", "createdby {id}"])
#test_query_membership_by_id = createByIdTest(tableName="memberships", queryEndpoint="membershipById")
#test_query_membership_page = createPageTest(tableName="memberships", queryEndpoint="membershipPage")

test_membership_insert = createFrontendQuery(query="""
    mutation($id: UUID!, $user_id: UUID!, $group_id: UUID!, $rbac_id: UUID!) { 
        result: membershipInsert(membership: {id: $id, user_id: $user_id, group_id: $group_id, rbacobject: $rbac_id}) { 
            id
            msg
            membership {
                id
                membership_id
                group_id
                lastchange
                created
                valid
                                       
                changedby { id }
                rbacobject { id }                
            }
        }
    }
    """, 
    variables={"id": "ccde3a8b-81d0-4e2b-9aac-42e0eb2255b3", "user_id": "c9021902-c425-4710-8e4c-88ee9c9ea224", "group_id": "c9021902-c425-4710-8e4c-88ef9c9ea224", "rbac_id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003"},
    asserts=[]
)

test_membership_update = createUpdateQuery(
    query="""
        mutation($id: UUID!, $name: String!, $lastchange: DateTime!) {
            membershipUpdate(membership: {id: $id, user_id: $user_id, lastchange: $lastchange}) {
                result: membershipInsert(membership: {id: $id, user_id: $user_id, group_id: $group_id, rbacobject: $rbac_id}) { 
                    id
                    msg
                    membership {
                        id
                        membership_id
                        group_id
                        lastchange
                        created
                        valid
                                            
                        changedby { id }
                        rbacobject { id }                
                    }
                }
            }
        }
    """,
    variables={"id": "190a578c-afb1-11ed-9bd8-0242ac110002", "user_id": "0baae3db-d526-4b8a-a326-87da6507d935", "group_id": "0baae3db-d526-4b7a-a326-87da6507d935"},
    tableName="memberships"
)


