import os
from pathlib import Path

from antarest.main import flask_app


def get_env_var(env_var_name: str) -> str:
    env_var = os.getenv(env_var_name)
    if env_var is None:
        raise EnvironmentError(f"API need the env var: {env_var_name}.")
    return env_var


env_var_conf_path = get_env_var("ANTAREST_CONF")
conf_path = Path(env_var_conf_path)

app = flask_app(conf_path)

app.config["DEBUG"] = False
