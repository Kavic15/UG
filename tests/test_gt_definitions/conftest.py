import logging
import datetime
import pytest_asyncio
import uuid

@pytest_asyncio.fixture
async def GQLInsertQueries():
    result = {
        "events": {
            "create": """
mutation ($id: UUID!, $name: String!, $eventtype_id: UUID!, $name_en: String!) {
  eventInsert(
    event: {id: $id, name: $name, eventtypeId: $type_id, nameEn: $name_en}
  ) {
    id
    msg
  }
}""",
            "read": """query($id: UUID!){ result: eventById(id: $id) { id }}""",
},
        "eventcategories": {"create": """
mutation ($id: UUID!, $name: String!) {
  eventCategoryInsert(
    eventCategory: {id: $id, name: $name}
  ) {
    id
    msg
  }
}""",
            "read": """query($id: UUID!){ result: eventCategoryById(id: $id) { id }}""",
},
        "events_groups":{"create": """
mutation ($event_id: UUID!, $group_id: UUID!) {
  eventGroupInsert(
    eventGroup: {eventId: $event_id, groupId: $group_id}
  ) {
    id
    msg
  }
}""",
            "read": """query($id: UUID!){ result: eventGroupById(id: $id) { id }}""",
},
        "eventtypes": {"create": """
mutation ($id: UUID!, $name: String!, $category_id: UUID!) {
  eventTypeInsert(
    eventType: {id: $id, name: $name, categoryId: $category_id}
  ) {
    id
    msg
  }
}""",
            "read": """query($id: UUID!){ result: eventTypeById(id: $id) { id }}""",
},
        "eventinvitationtypes": {"create": """
mutation ($id: UUID!, $name: String!) {
  invitationTypeInsert(
    invitationType: {id: $id, name: $name }
  ) {
    id
    msg
  }
}""",
            "read": """query($id: UUID!){ result: invitationTypeById(id: $id) { id }}""",
},
        "events_users": {"create": """
mutation ($user_id: UUID!, $event_id: UUID!, $invitationtype_id: UUID!, $presencetype_id: UUID!) {
  presenceInsert(
    presence: {userId: $user_id, eventId: $event_id, invitationtypeId: $invitationtype_id, presencetypeId: $presencetype_id}
  ) {
    id
    msg
  }
}""",
            "read": """query($id: UUID!){ result: presenceById(id: $id) { id }}""",
},
      "eventpresencetypes": {"create": """
mutation ($id: UUID!, $name: String!) {
  presenceTypeInsert(
    presenceType: {id: $id, name: $name}
  ) {
    id
    msg
  }
}""",
            "read": """query($id: UUID!){ result: presenceTypeById(id: $id) { id }}""",
},

    }
    
    return result


@pytest_asyncio.fixture
async def FillDataViaGQL(DemoData, GQLInsertQueries, ClientExecutorAdmin):
    types = [type(""), type(datetime.datetime.now()), type(uuid.uuid1())]
    for tablename, queryset in GQLInsertQueries.items():
        table = DemoData.get(tablename, None)
        assert table is not None, f"{tablename} is missing in DemoData"

        for row in table:
            variable_values = {}
            for key, value in row.items():
                variable_values[key] = value
                if isinstance(value, datetime.datetime):
                    variable_values[key] = value.isoformat()
                elif type(value) in types:
                    variable_values[key] = f"{value}"

            readResponse = await ClientExecutorAdmin(query=queryset["read"], variable_values=variable_values)
            if readResponse["data"]["result"] is not None:
                logging.info(f"row with id `{variable_values['id']}` already exists in `{tablename}`")
                continue
            insertResponse = await ClientExecutorAdmin(query=queryset["create"], variable_values=variable_values)
            assert insertResponse.get("errors", None) is None, insertResponse
        logging.info(f"{tablename} initialized via gql query")
    logging.info(f"All WANTED tables are initialized")