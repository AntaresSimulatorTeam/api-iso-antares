import logging
import os
import sys
from pathlib import Path

from antarest.common.config import Config


def get_default_config_path() -> Path:
    config = Path("config.yaml")
    if config.exists():
        return config

    config = Path.home() / ".antares/config.yaml"
    if config.exists():
        return config

    raise ValueError(
        "Config file not found. Set it by '-c' with command line or place it at ./config.yaml or ~/.antares/config.yaml"
    )


def get_local_path() -> Path:
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        return Path(sys._MEIPASS)  # type: ignore
    except Exception:
        return Path(os.path.abspath(""))


def configure_logger(config: Config) -> None:
    logging_path = config.logging.path
    logging_level = config.logging.level or "INFO"
    logging_format = (
        config.logging.format
        or "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logging.basicConfig(
        filename=logging_path, format=logging_format, level=logging_level
    )

