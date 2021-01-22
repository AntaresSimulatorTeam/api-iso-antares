from storage_api.filesystem.config.model import Config
from storage_api.filesystem.folder_node import FolderNode
from storage_api.filesystem.inode import TREE
from storage_api.filesystem.root.input.thermal.series.area.area import (
    InputThermalSeriesArea,
)


class InputThermalSeries(FolderNode):
    def build(self, config: Config) -> TREE:
        children: TREE = {
            a: InputThermalSeriesArea(config.next_file(a), area=a)
            for a in config.area_names()
        }
        return children