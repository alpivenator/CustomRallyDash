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
- Interactive theme selector.
- Standalone 60 Hz mock telemetry generator for live preview.
- Raspberry Pi shift-light LEDs via `gpiozero` (optional).
- Full visual customization through `settings.py` (colours, fonts, sizes,
  scaling, overlay position).

## Requirements

- Python **3.12.x** (Python 3.13 and newer are not supported)
- `pygame==2.6.1`
- Raspberry Pi shift lights: `gpiozero==2.0.1` (optional)

## Getting Started

### Windows (Quick Start)

1. **Install Python 3.12**: Install Python 3.12 x64 and make sure the Python Launcher (`py`) is added to PATH.
2. **Run Installer**: Double-click `install.bat`. It creates a `.venv`, installs dependencies, and launches the interactive setup wizard.
3. **Setup Wizard**:
   - Select your language (English or Turkish).
   - Enter your dashboard machine's IP (default `127.0.0.1` for local setup, or local LAN IP like `192.168.1.x` for remote).
   - Select dashboard style (`digital` or `analog`) and overlay mode.
4. **Launch Dashboard**: Double-click `run_dash.bat` (or test UDP reception using `check_telemetry.bat`).

### Linux & Manual Setup

1. **Clone repository and set up virtual environment**:
   ```sh
   git clone https://github.com/alpivenator/Telemetry-Dashboard-for-Dirt-Rally-2.0.git
   cd Telemetry-Dashboard-for-Dirt-Rally-2.0
   python3.12 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run Interactive Setup or Launch Directly**:
   ```sh
   # Run setup wizard
   python tools/setup_wizard.py

   # Launch dashboard
   python main.py

   # Or preview instantly with synthetic telemetry
   python main.py --mock
   ```

### DiRT Rally 2.0 Telemetry Setup

The game telemetry configuration is stored at:
`Documents\My Games\DiRT Rally 2.0\hardwaresettings\hardware_settings_config.xml`.

Ensure the `<udp>` block has `enabled="true"`, `extradata="3"`, and `port="20777"`. See [CONFIGURATION.md](docs/CONFIGURATION.md) for full manual configuration details and firewall guidelines.

## Configuration

- `config.py` — system & hardware settings (network IP/port, LEDs, overlay behaviour).
- `settings.py` — visual layout & styling (colours, fonts, sizes, positions).
- `tools/telemetry_check.py` / `check_telemetry.bat` — UDP connection diagnostic.
- `tools/theme_selector.py` / `select_theme.bat` — Interactive theme switcher.

See [CONFIGURATION.md](docs/CONFIGURATION.md) for a full reference.

## Docs

- [ARCHITECTURE.md](docs/ARCHITECTURE.md) — Technical structure and data flow
- [CONFIGURATION.md](docs/CONFIGURATION.md) — Complete configuration and setup guide
- [CHANGELOG.md](docs/CHANGELOG.md) — Version change history ([CHANGELOG_TR.md](docs/CHANGELOG_TR.md) for Turkish)
- [ROADMAP.md](docs/ROADMAP.md) — Planned milestones ([ROADMAP_TR.md](docs/ROADMAP_TR.md) for Turkish)

## License

This project is licensed under the **GPL-3.0** license. See
[LICENSE](LICENSE).
