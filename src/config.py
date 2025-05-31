import os
import json
from typing import Dict
from constants import CONFIG_FILE

def load_config() -> Dict:
    default_config = {
        "midi_port": None,
        "secondary_midi_port": None,
        "auto_start": False,
        "custom_button_label": "",
        "custom_button_url": ""
    }
    if not CONFIG_FILE or not CONFIG_FILE.endswith(".json"):
        raise ValueError("Invalid config path")

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
