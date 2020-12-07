from typing import List, Optional

from api_iso_antares.custom_types import JSON, SUB_JSON
from api_iso_antares.domain.study.config import Config
from api_iso_antares.domain.study.inode import INode


class RawFileNode(INode[str]):
    def __init__(self, config: Config):
        self.config = config

    def get(self, url: Optional[List[str]] = None) -> str:
        self._assert_url(url)

        file_path = "/".join(self.config.path.absolute().parts)
        root_path = "/".join(self.config.root_path.parent.absolute().parts)
        file_relative = file_path.replace(root_path, "")
        return f"file{file_relative}"

    def save(self, data: str, url: Optional[List[str]] = None) -> None:
        self._assert_url(url)
        self.config.path.write_text(data)

    def validate(self, data: str) -> None:
        pass  # no validation

    def _assert_url(self, url: Optional[List[str]] = None) -> None:
        url = url or []
        if len(url) > 0:
            raise ValueError(
                f"url should be fully resolved when arrives on {self.__class__.__name__}"
            )
