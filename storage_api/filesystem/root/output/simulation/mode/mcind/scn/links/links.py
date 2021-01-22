from storage_api.filesystem.config.model import Config
from storage_api.filesystem.folder_node import FolderNode
from storage_api.filesystem.inode import TREE
from storage_api.filesystem.root.output.simulation.mode.mcind.scn.links.item.item import (
    OutputSimulationModeMcIndScnLinksItem as Item,
)


class _OutputSimulationModeMcIndScnLinksBis(FolderNode):
    def __init__(self, config: Config, area: str):
        FolderNode.__init__(self, config)
        self.area = area

    def build(self, config: Config) -> TREE:
        children: TREE = {}
        for link in config.get_links(self.area):
            name = f"{self.area} - {link}"
            children[link] = Item(config.next_file(name), self.area, link)
        return children


class OutputSimulationModeMcIndScnLinks(FolderNode):
    def build(self, config: Config) -> TREE:
        children: TREE = {}

        for area in config.area_names():
            children[area] = _OutputSimulationModeMcIndScnLinksBis(
                config, area
            )

        return children