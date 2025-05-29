import time

log_buffer = []

def log(msg):
    timestamp = time.strftime("%H:%M:%S")
    entry = f"[{timestamp}] {msg}"
    print(entry)
    log_buffer.append(entry)
    if len(log_buffer) > 500:
        log_buffer.pop(0)
