from storage_api.filesystem.config.model import Config
from storage_api.filesystem.folder_node import FolderNode
from storage_api.filesystem.inode import TREE
from storage_api.filesystem.root.input.solar.prepro.prepro import (
    InputSolarPrepro,
)
from storage_api.filesystem.root.input.solar.series.series import (
    InputSolarSeries,
)


class InputSolar(FolderNode):
    def build(self, config: Config) -> TREE:
        children: TREE = {
            "prepro": InputSolarPrepro(config.next_file("prepro")),
            "series": InputSolarSeries(config.next_file("series")),
        }
        return children