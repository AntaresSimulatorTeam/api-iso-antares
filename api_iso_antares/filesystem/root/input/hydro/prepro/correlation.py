from api_iso_antares.filesystem.config.model import Config
from api_iso_antares.filesystem.ini_file_node import IniFileNode


class InputHydroPreproCorrelation(IniFileNode):
    def __init__(self, config: Config):
        types = {
            "general": {"mode": str},
            "0": {},
            "1": {},
            "2": {},
            "3": {},
            "4": {},
            "5": {},
            "6": {},
            "7": {},
            "8": {},
            "9": {},
            "10": {},
            "11": {},
        }
        IniFileNode.__init__(self, config, types)
