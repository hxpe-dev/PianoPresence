import json
import os
from constants import CONFIG_FILE
from typing import Dict

def load_config() -> Dict:
    default_config = {
        "midi_port": None,
        "secondary_midi_port": None,
        "auto_start": False
    }
    if not os.path.exists(CONFIG_FILE):
        save_config(default_config)
        return default_config
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            for key, value in default_config.items():
                config.setdefault(key, value)
            return config
    except json.JSONDecodeError:
        return default_config

def save_config(config: Dict):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
