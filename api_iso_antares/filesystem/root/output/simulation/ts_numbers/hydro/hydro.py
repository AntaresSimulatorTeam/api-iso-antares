from api_iso_antares.filesystem.config import Config
from api_iso_antares.filesystem.folder_node import FolderNode
from api_iso_antares.filesystem.inode import TREE
from api_iso_antares.filesystem.root.output.simulation.ts_numbers.hydro.area import (
    OutputSimulationTsNumbersHydroArea,
)


class OutputSimulationTsNumbersHydro(FolderNode):
    def __init__(self, config: Config):
        children: TREE = {
            area: OutputSimulationTsNumbersHydroArea(
                config.next_file(area + ".txt")
            )
            for area in config.area_names
        }
        FolderNode.__init__(self, config, children)