from pystray import Icon, Menu, MenuItem
from PIL import Image
from ports import choose_midi_port
from config import load_config, save_config
from discord_presence import clear_presence
from utils import resource_path
from startup import toggle_auto_start, is_auto_start_enabled
import tkinter as tk
from threading import Thread
import os
from tkinter.scrolledtext import ScrolledText
from log import log_buffer

def create_tray_icon():
    icon_path = resource_path("assets/icon.png")
    icon_img = Image.open(icon_path)
    menu = Menu(
        MenuItem("Show Logs", lambda: Thread(target=show_log_window).start()),
        MenuItem("Set Primary MIDI Port", set_primary_midi_port),
        MenuItem("Set Secondary MIDI Port", set_secondary_midi_port),
        MenuItem("Auto-Start at System Boot", toggle_auto_start, checked=lambda _: is_auto_start_enabled()),
        MenuItem("Set Custom Button", lambda: Thread(target=set_custom_button).start()),
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

def set_custom_button(icon=None, item=None):
    config = load_config()

    def submit():
        config["custom_button_label"] = label_entry.get().strip()
        config["custom_button_url"] = url_entry.get().strip()
        save_config(config)
        window.destroy()

    window = tk.Tk()
    window.title("Set Custom Button")
    window.geometry("400x175")

    tk.Label(window, text="Button Label:").pack(pady=(10, 0))
    label_entry = tk.Entry(window, width=40)
    label_entry.insert(0, config.get("custom_button_label", ""))
    label_entry.pack()

    tk.Label(window, text="Button URL:").pack(pady=(10, 0))
    url_entry = tk.Entry(window, width=40)
    url_entry.insert(0, config.get("custom_button_url", ""))
    url_entry.pack()

    tk.Label(window, text="This will take effect after an app restart").pack(pady=(10, 0))
    tk.Button(window, text="Save", command=submit).pack(pady=10)
    window.mainloop()

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

def on_quit(icon=None, item=None):
    clear_presence()
    os._exit(0)
