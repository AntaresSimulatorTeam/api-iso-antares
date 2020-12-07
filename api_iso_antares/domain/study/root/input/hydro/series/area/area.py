from api_iso_antares.domain.study.config import Config
from api_iso_antares.domain.study.folder_node import FolderNode
from api_iso_antares.domain.study.root.input.hydro.series.area.mod import (
    InputHydroSeriesAreaMod,
)
from api_iso_antares.domain.study.root.input.hydro.series.area.ror import (
    InputHydroSeriesAreaRor,
)


class InputHydroSeriesArea(FolderNode):
    def __init__(self, config: Config):
        children = {
            "mod": InputHydroSeriesAreaMod(config.next_file("mod.txt")),
            "ror": InputHydroSeriesAreaRor(config.next_file("ror.txt")),
        }
        FolderNode.__init__(self, children)
