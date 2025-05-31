import os
from collections import deque

APP_NAME = "PianoPresence"

if os.name == "nt":  # Windows
    base_dir = os.getenv("APPDATA")
else:  # macOS/Linux
    base_dir = os.path.expanduser("~/.config")

CONFIG_DIR = os.path.join(base_dir, APP_NAME)
os.makedirs(CONFIG_DIR, exist_ok=True)

CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DISCORD_CLIENT_ID = '1377570118908772352'
AFK_TIMEOUT = 10
NOTE_WINDOW_SECONDS = 5
RETRY_INTERVAL = 5

note_timestamps = deque()
last_note_time = 0
last_update = {"state": None, "details": None}
port_name = [None]  # mutable reference
rpc = [None]  # mutable reference
