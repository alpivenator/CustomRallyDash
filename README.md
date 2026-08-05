# DiRT Rally 2.0 Telemetry Dashboard

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

- Python **3.12 or newer**
- `pygame` (always)
- `gpiozero` — Raspberry Pi shift lights only (optional)

## Getting Started

1. **Install dependencies** (a virtual environment is recommended):

   ```sh
   pip install -r requirements.txt
   ```

2. **Configure the game**: enable UDP telemetry in DiRT Rally 2.0
   (Extradata=3, 60 Hz) and set the `ip` field in
   `hardware_settings_config.xml` inside the game's configuration folder
   (`My Documents\My Games\DiRT Rally 2.0\`) to the dashboard computer's LAN
   IP. Use `127.0.0.1` when running on the same machine — see
   [CONFIGURATION.md](CONFIGURATION.md) for a Windows Firewall note.

3. **Run the dashboard**:

   ```sh
   python main.py
   ```

## Configuration

- `config.py` — system settings (network, LEDs, overlay behaviour).
- `settings.py` — visual settings (colours, fonts, sizes, positions).

See [CONFIGURATION.md](CONFIGURATION.md) for a full reference.

## Docs

- [ARCHITECTURE.md](ARCHITECTURE.md) — how the project is structured
- [CONFIGURATION.md](CONFIGURATION.md) — all settings explained
- [CHANGELOG.md](CHANGELOG.md) — change history (TR)
- [ROADMAP.md](ROADMAP.md) — planned work (TR)

## License

This project is licensed under the **GPL-3.0** license. See
[LICENSE](LICENSE).
