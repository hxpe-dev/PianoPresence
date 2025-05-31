from pypresence import Presence
from config import load_config
from constants import DISCORD_CLIENT_ID, rpc, last_update
from log import log

def update_presence(state=None, details=None, start_time=None, small_image=None, small_text=None):
    try:
        if rpc[0] is None:
            rpc[0] = Presence(DISCORD_CLIENT_ID)
            rpc[0].connect()
        if state == last_update["state"] and details == last_update["details"]:
            return
        last_update["state"] = state
        last_update["details"] = details

        config = load_config()
        buttons = [{"label": "Get PianoPresence (GitHub)", "url": "https://github.com/hxpe-dev/PianoPresence"}]

        # Add custom button if valid
        label = config.get("custom_button_label", "").strip()
        url = config.get("custom_button_url", "").strip()
        if label and url:
            buttons.append({"label": label, "url": url})

        payload = {
            "large_image": "piano",
            "large_text": "Piano Presence 🎹",
            "buttons": buttons
        }

        if state: payload["state"] = state
        if details: payload["details"] = details
        if start_time: payload["start"] = int(start_time)
        if small_image: payload["small_image"] = small_image
        if small_text: payload["small_text"] = small_text
        rpc[0].update(**payload)
    except Exception as e:
        log(f"Discord RPC error: {e}")

def clear_presence():
    if rpc[0]:
        try:
            rpc[0].clear()
            rpc[0].close()
        except Exception as e:
            log(f"Error closing Discord RPC: {e}")
        finally:
            rpc[0] = None
