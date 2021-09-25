import json
from jsonschema import validate, ValidationError

def get_schema(schema_name: str):

    with open(f"./json_schemas/{schema_name}.json", "r") as js:
        schema = json.load(js)
        
    return schema

def validate_json(json_data, schema_name: str):
    schema = get_schema(schema_name)
    try:
        validate(json_data, schema)
    except ValidationError as e:
        return False, e.message
    return json_data, None