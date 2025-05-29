import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from log import log_buffer

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
