import threading
from pystray import Icon, Menu, MenuItem
from PIL import Image
from gui import show_log_window
from ports import choose_midi_port
from config import load_config, save_config
from discord_presence import clear_presence
from utils import resource_path
from startup import toggle_auto_start, is_auto_start_enabled
import os

def create_tray_icon():
    icon_path = resource_path("assets/icon.png")
    icon_img = Image.open(icon_path)
    menu = Menu(
        MenuItem("Show Logs", lambda: threading.Thread(target=show_log_window).start()),
        MenuItem("Set Primary MIDI Port", set_primary_midi_port),
        MenuItem("Set Secondary MIDI Port", set_secondary_midi_port),
        MenuItem("Auto-Start at System Boot", toggle_auto_start, checked=lambda _: is_auto_start_enabled()),
        MenuItem("Quit", on_quit)
    )
    tray = Icon("piano_presence", icon_img, "PianoPresence", menu)
    tray.run()

def set_primary_midi_port(icon=None, item=None):
    selected = choose_midi_port()
    if selected:
        config = load_config()
        config["midi_port"] = selected
        save_config(config)

def set_secondary_midi_port(icon=None, item=None):
    selected = choose_midi_port()
    if selected:
        config = load_config()
        config["secondary_midi_port"] = selected
        save_config(config)

def on_quit(icon=None, item=None):
    clear_presence()
    os._exit(0)
