import platform
from config import load_config, save_config

def toggle_auto_start(icon=None, item=None):
    config = load_config()
    config["auto_start"] = not config.get("auto_start", False)
    save_config(config)

    if is_windows():
        toggle_windows_startup(config["auto_start"])

def toggle_windows_startup(enable: bool):
    import winreg
    import sys
    key = winreg.HKEY_CURRENT_USER
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    app_name = "MIDI Presence"
    exe_path = sys.executable

    with winreg.OpenKey(key, reg_path, 0, winreg.KEY_ALL_ACCESS) as reg:
        if enable:
            winreg.SetValueEx(reg, app_name, 0, winreg.REG_SZ, exe_path)
        else:
            try:
                winreg.DeleteValue(reg, app_name)
            except FileNotFoundError:
                pass

def is_auto_start_enabled():
    config = load_config()
    return config.get("auto_start", False)

def is_windows():
    return platform.system() == "Windows"
