"""Configuration loader."""
import json
import os

DEFAULTS = {
    "data_file": "data/students.json",
    "export_dir": "exports",
    "log_file": "logs/app.log",
    "log_level": "INFO",
}


def load_config(path="config/config.json"):
    """Load settings from a JSON file. Fall back to defaults on any problem."""
    config = dict(DEFAULTS)
    if not os.path.exists(path):
        return config
    try:
        with open(path, "r", encoding="utf-8") as f:
            config.update(json.load(f))
    except (json.JSONDecodeError, OSError):
        pass  # Keep defaults. The caller logs nothing yet because logging is not set up.
    return config
