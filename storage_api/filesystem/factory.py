from pathlib import Path
from typing import Tuple

from storage_api.custom_types import JSON
from storage_api.filesystem.config.files import ConfigPathBuilder
from storage_api.filesystem.config.json import ConfigJsonBuilder
from storage_api.filesystem.config.model import Config
from storage_api.filesystem.root.study import Study


class StudyFactory:
    def create_from_fs(self, path: Path) -> Tuple[Config, Study]:
        config = ConfigPathBuilder.build(path)
        return config, Study(config)

    def create_from_config(self, config: Config) -> Study:
        return Study(config)

    def create_from_json(self, path: Path, json: JSON) -> Tuple[Config, Study]:
        config = ConfigJsonBuilder.build(path, json)
        return config, Study(config)