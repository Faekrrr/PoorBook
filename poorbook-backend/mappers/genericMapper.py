import sys
sys.path.append('.')
from pydantic import BaseModel
from typing import List

def genericSerialMapper(object) -> list:
    """ Map list of offers to list od dicts """
    return [genericMapper(value) for value in object]


def genericMapper(object) -> dict:
    """ Map values from given object to dict """
    result = {"id": str(object.pop("_id"))} if "_id" in object else {}
    for key, value in object.items():
        if isinstance(value, List):
            result[key] = [genericMapper(item.model_dump()) if isinstance(item, BaseModel) else item for item in value]
        else:
            result[key] = value
    return result

    
