from antarest.storage.repository.filesystem.config.model import StudyConfig
from antarest.storage.repository.filesystem.folder_node import FolderNode
from antarest.storage.repository.filesystem.inode import TREE
from antarest.storage.repository.filesystem.root.input.load.series.area import (
    InputLoadSeriesArea,
)


class InputLoadSeries(FolderNode):
    def build(self, config: StudyConfig) -> TREE:
        children: TREE = {
            f"load_{a}": InputLoadSeriesArea(config.next_file(f"load_{a}.txt"))
            for a in config.area_names()
        }
        return children
