# Telemetry Dashboard for DiRT Rally 2.0 

A real-time telemetry dashboard for **DiRT Rally 2.0**. The game broadcasts raw
UDP packets in the **Extradata=3** format at 60 Hz; this project captures,
decodes, and renders them live as a compact digital dash or an analog gauge —
optionally as a click-through overlay on Windows and/or mirrored to physical
shift lights on a Raspberry Pi.

## Features

- Digital dashboard (RPM bar, gear, speed, throttle/brake bars) and analog
  gauge dashboard (needle, dial ticks, dynamic redline).
- Windows click-through overlay with `alpha` and `chroma` transparency modes.
- Raspberry Pi shift-light LEDs via `gpiozero` (optional).
- Full visual customization through `settings.py` (colours, fonts, sizes,
  scaling, overlay position).

<!-- TODO: add screenshots -->

## Requirements

- Python **3.12.x** (Python 3.13 and newer are not supported)
- `pygame==2.6.1`
- Raspberry Pi shift lights: `gpiozero==2.0.1` (optional)

## Getting Started

1. **Install Python 3.12**: on Windows, install Python 3.12 x64 and make sure
   the Python Launcher (`py`) is available.

2. **Install the dashboard**: extract the project folder and run `install.bat`. The script creates a local `.venv`, installs pygame, and
   starts the first-run setup wizard.

3. **Complete the setup wizard**:
   - Choose your preferred language (English or Turkish).
   - Enter the dashboard computer's IPv4 address. `127.0.0.1` is the default
     when the game and dashboard run on the same computer.
   - For a remote device, enter the device's LAN IPv4 address,
     such as `192.168.1.x`. The wizard writes this same address to `config.py`
     and the game's telemetry XML.
   - Select the dashboard style and Windows overlay setting.
   - When setup completes, test the telemetry stream with `check_telemetry.bat`
     (or `python tools/telemetry_check.py`) while DiRT Rally 2.0 is running in a stage.
     The dashboard must be closed during the test.

For a manual installation, use a virtual environment and install the base
requirements:

   ```sh
   python -m pip install -r requirements.txt
   ```

The game file is normally located at
`Documents\My Games\DiRT Rally 2.0\hardwaresettings\hardware_settings_config.xml`.
The required UDP settings are `enabled="true"`, `extradata="3"`, and port
`20777`. See [CONFIGURATION.md](docs/CONFIGURATION.md) for manual configuration,
the telemetry check tool, and the Windows Firewall note.

## Configuration

- `config.py` — system settings (network, LEDs, overlay behaviour).
- `settings.py` — visual settings (colours, fonts, sizes, positions).
- `tools/telemetry_check.py` / `check_telemetry.bat` — UDP connection diagnostic.

The setup wizard edits selected values in `config.py` after creating a
timestamped backup. Visual settings remain manual and are edited in
`settings.py`.

See [CONFIGURATION.md](docs/CONFIGURATION.md) for a full reference.

## Docs

- [ARCHITECTURE.md](docs/ARCHITECTURE.md) — how the project is structured
- [CONFIGURATION.md](docs/CONFIGURATION.md) — all settings explained
- [CHANGELOG.md](docs/CHANGELOG.md) — change history (TR)
- [ROADMAP.md](docs/ROADMAP.md) — planned work (TR)

## License

This project is licensed under the **GPL-3.0** license. See
[LICENSE](LICENSE).
