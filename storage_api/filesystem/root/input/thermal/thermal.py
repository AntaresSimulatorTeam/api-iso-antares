from storage_api.filesystem.config.model import Config
from storage_api.filesystem.folder_node import FolderNode
from storage_api.filesystem.inode import TREE
from storage_api.filesystem.root.input.thermal.areas_ini import (
    InputThermalAreasIni,
)
from storage_api.filesystem.root.input.thermal.cluster.cluster import (
    InputThermalClusters,
)
from storage_api.filesystem.root.input.thermal.prepro.prepro import (
    InputThermalPrepro,
)
from storage_api.filesystem.root.input.thermal.series.series import (
    InputThermalSeries,
)


class InputThermal(FolderNode):
    def build(self, config: Config) -> TREE:
        children: TREE = {
            "clusters": InputThermalClusters(config.next_file("clusters")),
            "prepro": InputThermalPrepro(config.next_file("prepro")),
            "series": InputThermalSeries(config.next_file("series")),
            "areas": InputThermalAreasIni(config.next_file("areas.ini")),
        }
        return children