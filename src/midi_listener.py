import time
import mido
from mido import open_input
from constants import port_name, last_note_time, note_timestamps, NOTE_WINDOW_SECONDS, AFK_TIMEOUT
from discord_presence import update_presence, clear_presence
from log import log

def listen_for_midi_activity():
    global last_note_time, note_timestamps
    session_start_time = time.time()
    total_notes = 0
    try:
        with open_input(port_name[0]) as inport:
            log(f"Connected to {port_name[0]}")
            while True:
                now = time.time()
                if port_name[0] not in mido.get_input_names():
                    log(f"MIDI device '{port_name[0]}' disconnected.")
                    break
                for msg in inport.iter_pending():
                    if msg.type == 'note_on' and msg.velocity > 0:
                        last_note_time = now
                        note_timestamps.append(now)
                        total_notes += 1
                while note_timestamps and now - note_timestamps[0] > NOTE_WINDOW_SECONDS:
                    note_timestamps.popleft()
                if now - last_note_time > AFK_TIMEOUT:
                    update_presence("💤 AFK on piano", f"Total notes played: {total_notes}", session_start_time, "afk_icon", "AFK")
                else:
                    nps = len(note_timestamps) / NOTE_WINDOW_SECONDS
                    update_presence("🎹 Playing piano", f"{nps:.1f} notes/sec · 🎵 {total_notes} notes", session_start_time, "active_icon", "Playing")
                time.sleep(1)
    except Exception as e:
        log(f"Error in MIDI loop: {e}")
        clear_presence()

def monitor_keyboard():
    warned = False
    while True:
        inputs = mido.get_input_names()
        if port_name[0] in inputs:
            if warned:
                log(f"🎹 MIDI device '{port_name[0]}' reconnected.")
            warned = False
            listen_for_midi_activity()
        else:
            if not warned:
                log("Waiting for MIDI device...")
                warned = True
            clear_presence()
        time.sleep(5)
