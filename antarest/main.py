import argparse
import logging
import os
import sys
from numbers import Number
from pathlib import Path
from typing import Tuple, Any

from gevent import monkey  # type: ignore

from antarest.common.utils import get_default_config_path, get_local_path, configure_logger
from antarest.storage.business.watcher import Watcher

monkey.patch_all(thread=False)

from flask import Flask, render_template, json, request
from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.orm import sessionmaker, scoped_session  # type: ignore
from werkzeug.exceptions import HTTPException

from antarest import __version__
from antarest.eventbus.main import build_eventbus
from antarest.login.auth import Auth
from antarest.common.config import Config
from antarest.common.persistence import Base
from antarest.common.reverse_proxy import ReverseProxyMiddleware
from antarest.common.swagger import build_swagger
from antarest.launcher.main import build_launcher
from antarest.login.main import build_login
from antarest.storage.main import build_storage


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        dest="config_file",
        help="path to the config file",
    )
    parser.add_argument(
        "-v",
        "--version",
        dest="version",
        help="Server version",
        action="store_true",
        required=False,
    )
    return parser.parse_args()


def get_arguments() -> Tuple[Path, bool]:
    arguments = parse_arguments()

    display_version = arguments.version or False
    if display_version:
        return Path("."), display_version

    config_file = Path(arguments.config_file or get_default_config_path())
    return config_file, display_version


def flask_app(config_file: Path) -> Flask:
    res = get_local_path() / "resources"
    config = Config.from_yaml_file(res=res, file=config_file)

    configure_logger(config)
    # Database
    engine = create_engine(config.db_url, echo=config.debug)
    Base.metadata.create_all(engine)
    db_session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )

    application = Flask(
        __name__, static_url_path="/static", static_folder=str(res / "webapp")
    )
    application.wsgi_app = ReverseProxyMiddleware(application.wsgi_app)  # type: ignore

    application.config["SECRET_KEY"] = config.security.jwt_key
    application.config["JWT_ACCESS_TOKEN_EXPIRES"] = Auth.ACCESS_TOKEN_DURATION
    application.config[
        "JWT_REFRESH_TOKEN_EXPIRES"
    ] = Auth.REFRESH_TOKEN_DURATION
    application.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]

    @application.route("/", methods=["GET"])
    def home() -> Any:
        """
        Home ui
        ---
        responses:
            '200':
              content:
                 application/html: {}
              description: html home page
        tags:
          - UI
        """
        return render_template("index.html")

    @application.teardown_appcontext
    def shutdown_session(exception: Any = None) -> None:
        Auth.invalidate()
        db_session.remove()

    @application.errorhandler(HTTPException)
    def handle_exception(e: Any) -> Tuple[Any, Number]:
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps(
            {
                "name": e.name,
                "description": e.description,
            }
        )
        response.content_type = "application/json"
        return response, e.code

    event_bus = build_eventbus(application, config)
    user_service = build_login(
        application, config, db_session, event_bus=event_bus
    )
    storage = build_storage(
        application,
        config,
        db_session,
        user_service=user_service,
        event_bus=event_bus,
    )

    build_launcher(
        application,
        config,
        db_session,
        service_storage=storage,
        event_bus=event_bus,
    )
    build_swagger(application)

    return application


if __name__ == "__main__":
    config_file, display_version = get_arguments()

    if display_version:
        print(__version__)
        sys.exit()
    else:
        app = flask_app(config_file)
        app.socketio.run(app, debug=False, host="0.0.0.0", port=8080)
