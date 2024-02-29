#import pytest
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

test_group_reference = createResolveReferenceTest(tableName="groups", gqltype="GroupGQLModel")
test_group_by_id = createByIdTest(tableName="groups", queryEndpoint="groupById")
test_group_page = createPageTest(tableName="groups", queryEndpoint="groupPage")

test_group_update = createUpdateQuery(tableName="groups", query="""mutation ($id: UUID!, $lastchange: DateTime!, $name: String!) {
  result: groupUpdate(group: {id: $id, lastchange: $lastchange, name: $name}) {
    id
    group {
      name
      lastchange
    }
  }
}""", variables={"id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003", "name": "newname"})

test_group_insert = createFrontendQuery(query="""mutation ($name: String!, $grouptype_id: UUID!) {
  result: groupInsert(group: {name: $name, grouptypeId: $grouptype_id }) {
    id
    msg
    group {
      name
      lastchange
      valid
      created
      grouptype {
        id
      }
      mastergroup {
        id
      }
      subgroups {
        id
      }
      memberships {
        id
      }
      roles {
        id
      }
    }
  }
}""", variables={"name": "newname", "grouptype_id": "cd49e157-610c-11ed-9312-001a7dda7110"},
    asserts=[])

#TODO
test_group_delete = createDeleteQuery(tableName="groups", queryBase="group", attributeNames=["id"], id="480f2802-a869-11ed-924c-0242ac110002")