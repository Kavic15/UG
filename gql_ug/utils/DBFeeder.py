import datetime
from functools import cache

from gql_ug.DBDefinitions import (
    GroupTypeModel, 
    RoleTypeModel,
    RoleCategoryModel,
    UserModel,
    GroupModel,
    MembershipModel,
    RoleModel,
)

from functools import cache

import os
import json
from uoishelpers.feeders import ImportModels
import datetime
import uuid

def get_demodata():
    def datetime_parser(json_dict):
        for (key, value) in json_dict.items():
            if key in ["startdate", "enddate", "lastchange", "created"]:
                if value is None:
                    dateValueWOtzinfo = None
                else:
                    try:
                        dateValue = datetime.datetime.fromisoformat(value)
                        dateValueWOtzinfo = dateValue.replace(tzinfo=None)
                    except:
                        print("jsonconvert Error", key, value, flush=True)
                        dateValueWOtzinfo = None
                
                json_dict[key] = dateValueWOtzinfo
            
            if (key in ["id", "changedby", "createdby", "rbacobject"]) or ("_id" in key):
                
                if key == "outer_id":
                    json_dict[key] = value
                elif value not in ["", None]:
                    json_dict[key] = uuid.UUID(value)
                else:
                    print(key, value)

        return json_dict


    with open("./systemdata.json", "r", encoding="utf-8") as f:
        jsonData = json.load(f, object_hook=datetime_parser)

    return jsonData

async def initDB(asyncSessionMaker):

    demoMode = os.environ.get("DEMO", "False")
    if demoMode == "False":
        dbModels = [
            GroupTypeModel,
            RoleCategoryModel,
            RoleTypeModel,
        ]
    else:
        dbModels = [
            GroupTypeModel,
            RoleCategoryModel,
            RoleTypeModel,
            UserModel,
            GroupModel,
            MembershipModel,
            RoleModel,
        ]
        
    jsonData = get_demodata()
    await ImportModels(asyncSessionMaker, dbModels, jsonData)
    pass