from storage_api.filesystem.config.model import Config
from storage_api.filesystem.folder_node import FolderNode
from storage_api.filesystem.inode import TREE
from storage_api.filesystem.root.input.thermal.cluster.area.area import (
    InputThermalClustersArea,
)


class InputThermalClusters(FolderNode):
    def build(self, config: Config) -> TREE:
        children: TREE = {
            a: InputThermalClustersArea(config.next_file(a), area=a)
            for a in config.area_names()
        }
        return children