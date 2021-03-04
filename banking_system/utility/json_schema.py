import json
import os

from django.conf import settings
from jsonschema import Draft7Validator


class JsonSchemaValidator:
    """
    JSON schema validator

    This class containing method provides validator JSON data using a JSON schema.

    Note - This class runs over the jsonschema package.
    """

    @classmethod
    def _load_the_schema(cls, schema):
        """
        This private method will load the schema file into the memory.
        """

        path = os.path.join(settings.JSON_SCHEMA_DIR, schema)
        with open(path) as file:
            schema = json.loads(file.read())
        return schema

    @classmethod
    def _filter_error_path(cls, path):
        """
        This method will only filter the path where the error occur.
        """

        if len(path) > 1:
            return " -> ".join(str(p) for p in path)
        else:
            return "".join(path)

    @classmethod
    def validate(cls, instance, schema):
        """
        This method will validate and return an list of error messages
        """

        schema = cls._load_the_schema(schema=schema)
        validator = Draft7Validator(schema=schema)
        return [
            f"{cls._filter_error_path(error.path)} {error.message}"
            for error in validator.iter_errors(instance)
        ]
