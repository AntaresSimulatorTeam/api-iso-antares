import pytest
import json

from jsonschema import ValidationError

from api_iso_antares.antares_io.data import validate

jsonschema_litteral = """
{
  "$id": "http://json-schema.org/draft-07/schema#",
  "$schema": "http://json-schema.org/draft-07/schema#",
  "description": "A small exemple.",
  "type": "object",
  "properties": {
    "part1": {
      "type": "object",
      "required": [
        "key_int",
        "key_str"
      ],
      "properties": {
        "key_int": {
          "type": "integer",
          "description": "A description"
        },
        "key_str": {
          "type": "string",
          "description": "An other description"
        }
      }
    },
    "part2": {
      "type": "object",
      "properties": {
        "key_bool": {
          "type": "boolean",
          "description": "A description"
        },
        "key_bool2": {
          "type": "boolean"
        }
      }
    }
  }
}
"""


def test_validate_json_ok() -> None:
    jsonschema = json.loads(jsonschema_litteral)

    jsondata = {
        "part1": {"key_int": 1, "key_str": "value1"},
        "part2": {"key_bool": True, "key_bool2": False},
    }

    validate(jsondata, jsonschema)


def test_validate_json_wrong_key() -> None:
    jsonschema = json.loads(jsonschema_litteral)

    jsondata = {
        "part1": {"WRONG_KEY": 1, "key_str": "value1"},
        "part2": {"key_bool": True, "key_bool2": False},
    }

    with pytest.raises(ValidationError):
        validate(jsondata, jsonschema)


def test_validate_json_wrong_type() -> None:
    jsonschema = json.loads(jsonschema_litteral)

    jsondata = {
        "part1": {"key_int": 1.9, "key_str": "value1"},
        "part2": {"key_bool": True, "key_bool2": False},
    }

    with pytest.raises(ValidationError):
        validate(jsondata, jsonschema)
