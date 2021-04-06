import argparse
import os
import threading
from pathlib import Path
from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from antarest.common.config import Config
from antarest.common.persistence import Base
from antarest.common.utils import get_default_config_path, get_local_path, configure_logger
from antarest.eventbus.main import build_eventbus_service
from antarest.login.main import build_login_service
from antarest.storage.business.watcher import Watcher
from antarest.storage.main import build_storage_service
from antarest.storage.service import StorageService


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        dest="config_file",
        help="path to the config file",
    )
    return parser.parse_args()


def watcher_task(config: Config, storage_service: StorageService):
    watcher = Watcher(config=config, service=storage_service)
    return watcher


def start_scheduled_tasks(config_file: Path):
    res = get_local_path() / "resources"
    config = Config.from_yaml_file(res=res, file=config_file)

    configure_logger(config)
    # Database
    engine = create_engine(config.db_url, echo=config.debug)
    Base.metadata.create_all(engine)
    db_session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )

    event_bus = build_eventbus_service(config)
    user_service = build_login_service(config, db_session, event_bus=event_bus)
    storage_service = build_storage_service(
        config,
        db_session,
        user_service,
        event_bus=event_bus,
    )

    watcher = watcher_task(config, storage_service)
    watcher.start()


if __name__ == "__main__":
    env_var_conf_path = os.getenv("ANTAREST_CONF")
    conf_path = (
        Path(env_var_conf_path) if env_var_conf_path is not None else None
    )
    args = parse_arguments()
    config_file = args.config_file or conf_path or get_default_config_path()
    start_scheduled_tasks(config_file)
    while True:
        sleep(1)
