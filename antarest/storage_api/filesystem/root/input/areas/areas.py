from antarest.storage_api.filesystem.config.model import Config
from antarest.storage_api.filesystem.folder_node import FolderNode
from antarest.storage_api.filesystem.inode import TREE
from antarest.storage_api.filesystem.root.input.areas.item.item import (
    InputAreasItem,
)
from antarest.storage_api.filesystem.root.input.areas.list import (
    InputAreasList,
)
from antarest.storage_api.filesystem.root.input.areas.sets import (
    InputAreasSets,
)


class InputAreas(FolderNode):
    def build(self, config: Config) -> TREE:
        children: TREE = {
            a: InputAreasItem(config.next_file(a)) for a in config.area_names()
        }
        children["list"] = InputAreasList(config.next_file("list.txt"))
        children["sets"] = InputAreasSets(config.next_file("sets.ini"))
        return children