#!/usr/bin/env python
import subprocess
import sys

from environs import Env

env = Env()
env.read_env()

if __name__ == "__main__":
    _component = sys.argv[1]
    match _component:
        case "web":
            _listen_host = env.str("API_LISTEN_HOST")
            _listen_port = env.int("API_LISTEN_PORT")
            _logger_level = env.str("API_LOGGER_LEVEL")

            subprocess.call(
                " ".join(
                    ["uvicorn", "web:app", "--reload", "--port", str(_listen_port), "--host", _listen_host,
                     "--log-level", _logger_level]
                ),
                shell=True,
            )
        case _:
            raise ValueError(f"Unknown component: {_component}")
