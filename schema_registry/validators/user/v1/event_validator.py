import json
import jsonschema
from pathlib import Path
from pydantic import BaseModel


class UserEventValidator:

    def __init__(self):
        self.path_to_schema = 'schema_registry/json_schemas/user'

    def validate_be_event_added(self, event: BaseModel) -> bool:
        path_to_schema = Path(self.path_to_schema, 'business', 'added', '1.json')
        with open(path_to_schema) as schema_file:
            schema = json.load(schema_file)
        try:
            jsonschema.validate(event.model_dump(), schema)
        except jsonschema.exceptions.ValidationError as exc:
            print(f'ValidationError: {exc}')
            return False
        except jsonschema.exceptions.SchemaError as exc:
            print(f'SchemaError: {exc}')
            return False
        else:
            check_name_version: bool = event.event_version == 1 and event.event_name == 'UserAdded'
        return check_name_version

    def validate_stream_event_created(self, event: BaseModel) -> bool:
        path_to_schema = Path(self.path_to_schema, 'stream', 'created', '1.json')
        with open(path_to_schema) as schema_file:
            schema = json.load(schema_file)
        try:
            jsonschema.validate(event.model_dump(), schema)
        except jsonschema.exceptions.ValidationError as exc:
            print(f'ValidationError: {exc}')
            return False
        except jsonschema.exceptions.SchemaError as exc:
            print(f'SchemaError: {exc}')
            return False
        else:
            check_name_version: bool = event.event_version == 1 and event.event_name == 'UserCreated'

        return check_name_version
