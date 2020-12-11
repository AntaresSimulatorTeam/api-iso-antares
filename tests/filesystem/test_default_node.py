from typing import Dict, List
from unittest.mock import Mock

import pytest

from api_iso_antares.filesystem.folder_node import FolderNode
from api_iso_antares.filesystem.inode import INode
from tests.filesystem.utils import TestSubNode


def build_tree() -> INode:
    config = Mock()
    config.path.exist.return_value = True
    return FolderNode(
        config=config,
        children={
            "input": TestSubNode(value=100),
            "output": TestSubNode(value=200),
        },
    )


@pytest.mark.unit_test
def test_get():
    tree = build_tree()

    res = tree.get(["input"])
    assert res == 100

    res = tree.get([])
    assert res == {"input": 100, "output": 200}


@pytest.mark.unit_test
def test_save():
    tree = build_tree()

    tree.save(105, ["output"])
    assert tree.get(["output"]) == 105

    tree.save({"input": 205})
    assert tree.get(["input"]) == 205
