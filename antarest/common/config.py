import os
from copy import deepcopy
from pathlib import Path
from typing import Any, Optional

import yaml

from antarest.common.custom_types import JSON


class Config:
    def __init__(self, data: Optional[JSON] = None):
        self.data = data or dict()

    def __getitem__(self, item: str) -> Any:
        return self._get(item)

    def _get(self, key: str) -> Any:
        parts = key.split(".")

        env = "_".join(parts).upper()
        if env in os.environ:
            return os.environ[env]

        data = deepcopy(self.data)
        for p in parts:
            if p not in data:
                return None
            data = data[p]
        return data


class ConfigYaml(Config):
    def __init__(self, file: Path, res: Optional[Path] = None):
        data = yaml.safe_load(open(file))
        data["_internal"] = {}
        data["_internal"]["resources_path"] = res
        Config.__init__(self, data)
