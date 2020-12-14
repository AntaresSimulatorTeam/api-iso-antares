from api_iso_antares.filesystem.config import Config
from api_iso_antares.filesystem.folder_node import FolderNode
from api_iso_antares.filesystem.inode import TREE
from api_iso_antares.filesystem.root.input.link.area.link import (
    InputLinkAreaLink,
)
from api_iso_antares.filesystem.root.input.link.area.properties import (
    InputLinkAreaProperties,
)


class InputLinkArea(FolderNode):
    def __init__(self, config: Config, area: str):
        children: TREE = {
            l: InputLinkAreaLink(config.next_file(f"{l}.txt"))
            for l in config.get_links(area)
        }
        children["properties"] = InputLinkAreaProperties(
            config.next_file("properties.ini"), area=area
        )

        FolderNode.__init__(self, config, children)