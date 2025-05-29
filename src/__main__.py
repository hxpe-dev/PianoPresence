from config import load_config, save_config
from log import log
from ports import choose_midi_port
from midi_listener import monitor_keyboard
from tray import create_tray_icon

import threading

def main():
    config = load_config()
    primary = config.get("midi_port")
    secondary = config.get("secondary_midi_port")

    from constants import port_name as global_port_name
    inputs = __import__("mido").get_input_names()

    if primary in inputs:
        global_port_name[0] = primary
    elif secondary in inputs:
        log(f"Primary MIDI port '{primary}' not found. Falling back to secondary: '{secondary}'")
        global_port_name[0] = secondary
    else:
        global_port_name[0] = primary or secondary
        log(f"Configured MIDI ports not available yet. Waiting for device '{global_port_name[0]}'...")

    if not global_port_name[0]:
        selected = choose_midi_port()
        if not selected:
            log("No MIDI device selected. Exiting.")
            return
        global_port_name[0] = selected
        config["midi_port"] = selected
        save_config(config)

    log(f"Monitoring MIDI port: {global_port_name[0]}")
    threading.Thread(target=monitor_keyboard, daemon=True).start()
    create_tray_icon()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        from discord_presence import clear_presence
        log("Stopped by user.")
        clear_presence()
