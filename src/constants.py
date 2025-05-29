from collections import deque

CONFIG_FILE = "config.json"
DISCORD_CLIENT_ID = '1377570118908772352'
AFK_TIMEOUT = 10
NOTE_WINDOW_SECONDS = 5
RETRY_INTERVAL = 5

note_timestamps = deque()
last_note_time = 0
last_update = {"state": None, "details": None}
port_name = [None]  # mutable reference
rpc = [None]  # mutable reference
