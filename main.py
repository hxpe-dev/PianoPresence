import threading
import time
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import mido
from mido import open_input
from pypresence import Presence
import json
import os
import logging
from collections import deque
from typing import Optional, Dict
import pystray
from PIL import Image
import sys

# --- Constants ---
CONFIG_FILE = "config.json"
DISCORD_CLIENT_ID = '1377570118908772352'
AFK_TIMEOUT = 10
NOTE_WINDOW_SECONDS = 5
RETRY_INTERVAL = 5

note_timestamps = deque()
rpc = None
last_note_time = 0
port_name = None
last_update = {"state": None, "details": None}

# --- Logging ---
log_buffer = []
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


def log(msg):
    timestamp = time.strftime("%H:%M:%S")
    entry = f"[{timestamp}] {msg}"
    print(entry)
    log_buffer.append(entry)
    if len(log_buffer) > 500:
        log_buffer.pop(0)


def load_config() -> Dict:
    if not os.path.exists(CONFIG_FILE):
        save_config({})
        return {}
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            return config if isinstance(config, dict) else {}
    except json.JSONDecodeError:
        return {}


def save_config(config: Dict):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)


def choose_midi_port() -> Optional[str]:
    inputs = mido.get_input_names()
    if not inputs:
        log("No MIDI input devices found.")
        return None

    selected = [None]

    def on_select():
        choice = listbox.curselection()
        if choice:
            selected[0] = inputs[choice[0]]
            win.destroy()

    win = tk.Tk()
    win.title("Select MIDI Input")
    win.geometry("400x250")
    tk.Label(win, text="Select a MIDI input port:").pack(pady=10)

    listbox = tk.Listbox(win)
    for name in inputs:
        listbox.insert(tk.END, name)
    listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    tk.Button(win, text="Connect", command=on_select).pack(pady=10)
    win.mainloop()

    return selected[0]


def update_presence(state=None, details=None, start_time=None, small_image=None, small_text=None):
    global rpc, last_update
    try:
        if rpc is None:
            rpc = Presence(DISCORD_CLIENT_ID)
            rpc.connect()
        if state == last_update["state"] and details == last_update["details"]:
            return
        last_update = {"state": state, "details": details}
        payload = {
            "large_image": "piano",
            "large_text": "MIDI Keyboard 🎹",
            "buttons": [{"label": "View on GitHub", "url": "https://github.com/hxpe-dev/PianoPresence"}]
        }
        if state: payload["state"] = state
        if details: payload["details"] = details
        if start_time: payload["start"] = int(start_time)
        if small_image: payload["small_image"] = small_image
        if small_text: payload["small_text"] = small_text
        rpc.update(**payload)
    except Exception as e:
        log(f"Discord RPC error: {e}")


def clear_presence():
    global rpc
    if rpc:
        try:
            rpc.clear()
            rpc.close()
        except Exception as e:
            log(f"Error closing Discord RPC: {e}")
        finally:
            rpc = None


def listen_for_midi_activity(port_name: str):
    global last_note_time, note_timestamps
    session_start_time = time.time()
    total_notes = 0
    try:
        with open_input(port_name) as inport:
            log(f"Connected to {port_name}")
            while True:
                now = time.time()
                if port_name not in mido.get_input_names():
                    log(f"MIDI device '{port_name}' disconnected.")
                    break
                for msg in inport.iter_pending():
                    if msg.type == 'note_on' and msg.velocity > 0:
                        last_note_time = now
                        note_timestamps.append(now)
                        total_notes += 1
                while note_timestamps and now - note_timestamps[0] > NOTE_WINDOW_SECONDS:
                    note_timestamps.popleft()
                if now - last_note_time > AFK_TIMEOUT:
                    update_presence(
                        state="💤 AFK on piano",
                        details=f"Total notes played: {total_notes}",
                        start_time=session_start_time,
                        small_image="afk_icon",
                        small_text="AFK"
                    )
                else:
                    nps = len(note_timestamps) / NOTE_WINDOW_SECONDS
                    update_presence(
                        state="🎹 Playing piano",
                        details=f"{nps:.1f} notes/sec · 🎵 {total_notes} notes",
                        start_time=session_start_time,
                        small_image="active_icon",
                        small_text="Playing"
                    )
                time.sleep(1)
    except Exception as e:
        log(f"Error in MIDI loop: {e}")
        clear_presence()


def monitor_keyboard():
    global port_name
    warned = False
    while True:
        inputs = mido.get_input_names()
        if port_name in inputs:
            if warned:
                log(f"🎹 MIDI device '{port_name}' reconnected.")
            warned = False
            listen_for_midi_activity(port_name)
        else:
            if not warned:
                log("Waiting for MIDI device...")
                warned = True
            clear_presence()
        time.sleep(RETRY_INTERVAL)


# --- GUI Log Window ---
def show_log_window():
    root = tk.Tk()
    root.title("MIDI Presence Logs")
    root.geometry("600x400")
    text_area = ScrolledText(root)
    text_area.pack(fill="both", expand=True)
    text_area.insert(tk.END, "\n".join(log_buffer))
    text_area.config(state="disabled")

    def refresh():
        text_area.config(state="normal")
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, "\n".join(log_buffer))
        text_area.config(state="disabled")
        root.after(2000, refresh)

    root.after(2000, refresh)
    root.mainloop()


def resource_path(relative_path):
    """ Get the absolute path to a resource in PyInstaller bundle """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# --- System Tray ---
def create_tray_icon():
    icon_path = resource_path("assets/icon.png")
    icon_img = Image.open(icon_path)
    menu = pystray.Menu(
        pystray.MenuItem("Show Logs", lambda: threading.Thread(target=show_log_window).start()),
        pystray.MenuItem("Quit", on_quit)
    )
    tray = pystray.Icon("midi_presence", icon_img, "MIDI Keyboard Presence", menu)
    tray.run()


def on_quit(icon=None, item=None):
    clear_presence()
    os._exit(0)


# --- Main ---
def main():
    global port_name
    config = load_config()
    port_name = config.get("midi_port")
    if not port_name or port_name not in mido.get_input_names():
        port_name = choose_midi_port()
        if not port_name:
            log("No MIDI device selected. Exiting.")
            return
        config["midi_port"] = port_name
        save_config(config)

    log(f"Monitoring MIDI port: {port_name}")
    threading.Thread(target=monitor_keyboard, daemon=True).start()
    create_tray_icon()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("Stopped by user.")
        clear_presence()
