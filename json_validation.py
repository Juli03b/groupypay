"Module to facilitate json validation"

import json
from jsonschema import validate, ValidationError
from exceptions.Bad_Request import Bad_Request

def get_schema(schema_name: str):
    """Opens and return json schema using name of schema"""
    with open(f"./json_schemas/{schema_name}_schema.json", "r", encoding="utf-8") as json_schema:
        schema = json.load(json_schema)

    return schema

def validate_json(json_data, schema_name: str):
    """Validates json and returns it if valid. Raises error if not valid"""
    schema = get_schema(schema_name)
    try:
        validate(json_data, schema)
        
    except ValidationError as error:        
        raise Bad_Request(error.message, "Invalid data") from error

    return json_data
