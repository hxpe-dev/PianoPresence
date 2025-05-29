import tkinter as tk
import mido
from log import log
from config import save_config, load_config

def choose_midi_port():
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
