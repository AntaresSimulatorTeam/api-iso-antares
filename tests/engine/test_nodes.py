from pathlib import Path
from unittest.mock import Mock

from api_iso_antares.antares_io.reader import IniReader
from api_iso_antares.antares_io.validator import JsmValidator
from api_iso_antares.engine.nodes import (
    MixFolderNode,
    IniFileNode,
    NodeFactory,
)
from api_iso_antares.jsonschema import JsonSchema


def test_mix_folder_with_zones_list(project_path: Path) -> None:
    path = project_path / "tests/engine/resources/s1/areas"
    jsm = {
        "$schema": "http://json-schema.org/draft-07/schema",
        "type": "object",
        "rte-metadata": {"strategy": "S1"},
        "properties": {
            "list": {
                "type": "string",
            },
            "sets": {
                "type": "string",
            },
        },
        "additionalProperties": {"type": "string"},
    }
    content = "Hello, World"
    expected = {
        "list": content,
        "sets": content,
        "fr": content,
        "de": content,
        "it": content,
        "es": content,
    }

    node = Mock()
    node.get_content.return_value = content
    node.get_filename.side_effect = ["list.txt", "sets.ini"]
    factory = Mock()
    factory.build.return_value = node

    node = MixFolderNode(
        path=path,
        jsm=JsonSchema(jsm),
        ini_reader=Mock(),
        parent=None,
        node_factory=factory,
    )
    json_data = node.get_content()

    assert expected == json_data


def test_mix_keys_in_ini_file(project_path: str):
    path = (
        project_path
        / "tests/engine/resources/s2/input/bindingconstraints/bindingconstraints.ini"
    )
    jsm = {
        "$schema": "http://json-schema.org/draft-07/schema",
        "type": "object",
        "additionalProperties": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "id": {"type": "string"},
                "enabled": {"type": "boolean"},
                "type": {"type": "string"},
                "operator": {"type": "string"},
            },
            "additionalProperties": {"type": "number"},
        },
    }

    node = IniFileNode(
        path=path,
        jsm=JsonSchema(jsm),
        ini_reader=IniReader(),
        parent=None,
        node_factory=Mock(),
    )
    json_data = node.get_content()

    assert json_data["0"]["east%north"] == -1
    assert json_data["1"]["east%west"] == 1

    jsm_validator = JsmValidator(jsm=JsonSchema(jsm))
    jsm_validator.validate(json_data)


def test_mix_file_with_zones_list(project_path: Path) -> None:
    path = project_path / "tests/engine/resources/s3/input/bindingconstraints"
    jsm = {
        "$schema": "http://json-schema.org/draft-07/schema",
        "type": "object",
        "rte-metadata": {"strategy": "S3"},
        "properties": {
            "bindingconstraints": {
                "rte-metadata": {"filename": "bindingconstraints.ini"},
                "additionalProperties": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "id": {"type": "string"},
                        "enabled": {"type": "boolean"},
                        "type": {"type": "string"},
                        "operator": {"type": "string"},
                    },
                    "additionalProperties": {"type": "number"},
                },
            }
        },
        "additionalProperties": {"type": "string"},
    }

    node = MixFolderNode(
        path=path,
        jsm=JsonSchema(jsm),
        ini_reader=Mock(),
        parent=None,
        node_factory=NodeFactory({"default": IniReader()}),
    )
    json_data = node.get_content()

    assert json_data["northern mesh.txt"] == str(
        Path("file/bindingconstraints/northern mesh.txt")
    )