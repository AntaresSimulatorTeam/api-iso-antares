from antarest.storage.repository.filesystem.config.model import StudyConfig
from antarest.storage.repository.filesystem.ini_file_node import IniFileNode


class GeneralData(IniFileNode):
    TYPES = {
        "general": {
            "mode": str,
            "horizon": (int, str),
            "nbyears": int,
            "simulation.start": int,
            "simulation.end": int,
            "january.1st": str,
            "first-month-in-year": str,
            "first.weekday": str,
            "leapyear": bool,
            "year-by-year": bool,
            "derated": bool,
            "custom-ts-numbers": bool,
            "user-playlist": bool,
            "filtering": bool,
            "active-rules-scenario": str,
            "generate": str,
            "nbtimeseriesload": int,
            "nbtimeserieshydro": int,
            "nbtimeserieswind": int,
            "nbtimeseriesthermal": int,
            "nbtimeseriessolar": int,
            "refreshtimeseries": str,
            "intra-modal": str,
            "inter-modal": str,
            "refreshintervalload": int,
            "refreshintervalhydro": int,
            "refreshintervalwind": int,
            "refreshintervalthermal": int,
            "refreshintervalsolar": int,
            "readonly": bool,
        },
        "input": {"import": str},
        "output": {
            "synthesis": bool,
            "storenewset": bool,
            "archives": str,
        },
        "optimization": {
            "simplex-range": str,
            "transmission-capacities": bool,
            "link-type": str,
            "include-constraints": bool,
            "include-hurdlecosts": bool,
            "include-tc-minstablepower": bool,
            "include-tc-min-ud-time": bool,
            "include-dayahead": bool,
            "include-strategicreserve": bool,
            "include-spinningreserve": bool,
            "include-primaryreserve": bool,
            "include-exportmps": bool,
        },
        "other preferences": {
            "initial-reservoir-levels": str,
            "power-fluctuations": str,
            "shedding-strategy": str,
            "shedding-policy": str,
            "unit-commitment-mode": str,
            "number-of-cores-mode": str,
            "day-ahead-reserve-management": str,
        },
        "advanced parameters": {
            "accuracy-on-correlation": str,
            "adequacy-block-size": int,
        },
        "seeds - Mersenne Twister": {
            "seed-tsgen-wind": int,
            "seed-tsgen-load": int,
            "seed-tsgen-hydro": int,
            "seed-tsgen-thermal": int,
            "seed-tsgen-solar": int,
            "seed-tsnumbers": int,
            "seed-unsupplied-energy-costs": int,
            "seed-spilled-energy-costs": int,
            "seed-thermal-costs": int,
            "seed-hydro-costs": int,
            "seed-initial-reservoir-levels": int,
        },
    }

    def __init__(self, config: StudyConfig):
        IniFileNode.__init__(self, config, types=GeneralData.TYPES)
