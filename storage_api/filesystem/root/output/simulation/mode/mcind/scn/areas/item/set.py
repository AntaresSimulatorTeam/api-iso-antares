from storage_api.filesystem.config.model import Config
from storage_api.filesystem.folder_node import FolderNode
from storage_api.filesystem.inode import TREE
from storage_api.filesystem.root.output.simulation.mode.mcind.scn.areas.item.values import (
    OutputSimulationModeMcIndScnAreasItemValues as Values,
)


class OutputSimulationModeMcIndScnAreasSet(FolderNode):
    def __init__(self, config: Config, set: str):
        FolderNode.__init__(self, config)
        self.set = set

    def build(self, config: Config) -> TREE:
        children: TREE = dict()

        for timing in config.get_filters_year(self.set):
            children[f"values-{timing}"] = Values(
                config.next_file(f"values-{timing}.txt")
            )

        return children