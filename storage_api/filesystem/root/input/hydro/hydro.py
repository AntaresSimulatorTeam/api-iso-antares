from storage_api.filesystem.config.model import Config
from storage_api.filesystem.folder_node import FolderNode
from storage_api.filesystem.inode import TREE
from storage_api.filesystem.root.input.hydro.allocation.allocation import (
    InputHydroAllocation,
)
from storage_api.filesystem.root.input.hydro.common.common import (
    InputHydroCommon,
)
from storage_api.filesystem.root.input.hydro.hydro_ini import (
    InputHydroIni,
)
from storage_api.filesystem.root.input.hydro.prepro.prepro import (
    InputHydroPrepro,
)
from storage_api.filesystem.root.input.hydro.series.series import (
    InputHydroSeries,
)


class InputHydro(FolderNode):
    def build(self, config: Config) -> TREE:
        children: TREE = {
            "allocation": InputHydroAllocation(config.next_file("allocation")),
            "common": InputHydroCommon(config.next_file("common")),
            "prepro": InputHydroPrepro(config.next_file("prepro")),
            "series": InputHydroSeries(config.next_file("series")),
            "hydro": InputHydroIni(config.next_file("hydro.ini")),
        }
        return children