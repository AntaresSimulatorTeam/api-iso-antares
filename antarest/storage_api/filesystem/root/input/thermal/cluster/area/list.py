from antarest.storage_api.filesystem.config.model import Config
from antarest.storage_api.filesystem.ini_file_node import IniFileNode


class InputThermalClustersAreaList(IniFileNode):
    def __init__(self, config: Config, area: str):
        section = {
            "name": str,
            "group": str,
            "unitcount": int,
            "nominalcapacity": float,
            "market-bid-cost": float,
        }
        types = {ther: section for ther in config.get_thermals(area)}
        IniFileNode.__init__(self, config, types)