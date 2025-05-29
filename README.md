<p align="center">
  <strong><em><a href="#">🎹 PianoPresence</a></em></strong>
</p>
<p align="center">
  <a href="https://github.com/hxpe-dev/PianoPresence/releases"><img src="https://img.shields.io/github/downloads/hxpe-dev/PianoPresence/total?color=%233DDC84&logo=android&logoColor=%23fff&style=for-the-badge"></a>
  <a href="https://github.com/hxpe-dev/PianoPresence/releases"><img src="https://img.shields.io/github/v/release/hxpe-dev/PianoPresence?style=for-the-badge&logo=github"></a>
  <a href="https://github.com/hxpe-dev/PianoPresence/commits"><img src="https://img.shields.io/github/last-commit/hxpe-dev/PianoPresence?style=for-the-badge&logo=github"></a>
</p>

# **PianoPresence 🎹**

PianoPresence is a lightweight desktop application that integrates your MIDI keyboard activity with Discord Rich Presence, showing your playing status live on Discord — including notes per second, total notes, and idle (AFK) state.

---

## Features

- Detects connected MIDI keyboards and monitors note activity in real-time
- Displays live stats on Discord Rich Presence (notes/sec, total notes played)
- Auto-updates presence when idle or active
- Runs quietly in the system tray with customizable icon
- Tray menu options to show logs or quit the app
- Automatically reconnects when MIDI device is unplugged and plugged back
- Supports Windows (tested); Linux/macOS compatibility may vary

---

## Download & Installation

### Ready-to-Use Executable

You can download the latest prebuilt **Windows executable** from the [Releases page](https://github.com/hxpe-dev/PianoPresence/releases).  
Simply download, run the `.exe`, and it will start minimized to your system tray.

No installation or dependencies required for end users.

---

### For Developers / Running from Source

If you want to modify or run the project from source, you will need to install dependencies:

```bash
pip install -r requirements.txt
```
Then run:
```bash
python main.py
```
If you want to build your `.exe` file, you will need to install `pyinstaller`:
```bash
pip install pyinstaller
```
Then run:
```bash
pyinstaller main.spec
```

## Usage
- On first run, select your MIDI device when prompted.
- The app will run in the background with a tray icon.
- Right-click the tray icon to open the live logs or quit the app.
- Discord Rich Presence will update automatically based on your playing.

## Configuration
- Selected MIDI device is saved in `config.json`.
- Replace `icon.png` to customize the tray icon.
- Logs can be viewed anytime from the tray menu.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

## License
[MIT License](LICENSE.md)

---

Made with ❤️ by hxpe-dev