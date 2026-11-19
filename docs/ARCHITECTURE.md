# Architecture: CustomRallyDash

[Türkçe](ARCHITECTURE_TR.md) | **English**

CustomRallyDash is a real-time telemetry dashboard and overlay for DiRT Rally 2.0. The game broadcasts 264-byte UDP packets in the `Extradata=3` format at 60 Hz. The application captures these packets, decodes the telemetry fields, and draws either a compact digital HUD or a circular analog gauge. On Windows, the window can run as a click-through overlay on top of the game; on a Raspberry Pi, physical GPIO shift lights can mirror the engine RPM.

## Directory structure and file roles

```text
CustomRallyDash/
├── .github/
│   ├── workflows/
│   │   └── ci.yml            # GitHub Actions CI (ruff, pytest, pip-audit)
│   └── ISSUE_TEMPLATE/       # Bug report and feature request forms
├── core/
│   ├── __init__.py           # Package exports for telemetry and platform helpers
│   ├── udp_listener.py       # UDP socket listener and Extradata=3 packet decoder
│   ├── overlay_win.py        # Windows Win32 ctypes overlay helpers
│   └── led_controller.py     # Raspberry Pi GPIO shift-light driver (gpiozero)
├── dashboards/
│   ├── __init__.py           # Package exports for dashboard runners
│   ├── digital_dash.py       # Compact digital dashboard (600x200 px)
│   ├── analog_dash.py        # Analog gauge dashboard (600x350 px)
│   └── themes.py             # Motorsport and simulator color theme presets
├── docs/                     # Architecture, configuration, roadmap, and changelog
├── images/                   # WebP preview screenshots
├── tests/                    # Unit tests (pytest)
├── tools/
│   ├── __init__.py           # Package exports for setup and diagnostic utilities
│   ├── cli_ui.py             # Shared Rich panels/tables and arrow-key CLI prompts
│   ├── setup_wizard.py       # Bilingual first-run CLI setup wizard
│   ├── telemetry_check.py    # UDP connectivity diagnostic tool
│   ├── mock_telemetry.py     # 60 Hz synthetic UDP packet generator
│   └── theme_selector.py     # Interactive CLI theme switcher
├── config.py                 # System and hardware configuration
├── settings.py               # Visual layout and styling configuration
├── main.py                   # Unified entry point (supports --mock)
├── pyproject.toml            # Project metadata, Ruff/Black, and pytest settings
├── requirements.txt          # Base Python dependencies (pygame, rich, questionary)
├── requirements-pi.txt       # Optional Raspberry Pi dependency (gpiozero)
├── LICENSE                   # MIT license
├── README.md                 # Project overview and quick start (English)
├── README_TR.md              # Project overview and quick start (Turkish)
├── install.bat               # Windows environment setup and wizard launcher
├── install.sh                # Linux/Raspberry Pi setup and wizard launcher
├── run_dash.bat              # Windows dashboard launcher
├── run_mock.bat              # Windows mock telemetry launcher
├── select_theme.bat          # Windows theme selector launcher
└── check_telemetry.bat       # Windows telemetry check launcher
```

| Module / file | Responsibility |
| :--- | :--- |
| `main.py` | Application entry point. Reads `config.DASH_STYLE`, optionally starts the `--mock` broadcaster thread, and runs the chosen dashboard. |
| `config.py` | Non-visual settings: listen IP/port, LED toggle, overlay toggle, and dashboard style. Edited directly or via `setup_wizard.py`. |
| `settings.py` | Visual settings: base resolution, scaling factor, colors, font sizes, and overlay placement. Edited directly or via `theme_selector.py`. |
| `core/udp_listener.py` | Receives 264-byte UDP packets, unpacks 66 floats via `struct.unpack("66f", ...)`, and returns `TelemetryData`. |
| `core/overlay_win.py` | Win32 (`ctypes`) window styling for borderless, transparent, click-through overlays. |
| `core/led_controller.py` | Drives Raspberry Pi GPIO shift lights via `gpiozero` when `config.ENABLE_LEDS` is `True`. |
| `dashboards/digital_dash.py` | Digital HUD (600x200 px) with RPM bar, gear readout, speed, and pedal bars. |
| `dashboards/analog_dash.py` | Analog gauge (600x350 px) with trigonometric needle smoothing, tick marks, dynamic redline sector, and central gear dial. |
| `dashboards/themes.py` | Five color presets (`modern_dark`, `subaru_classic`, `gt3_racing`, `night_neon`, `retro_amber`). |
| `tools/cli_ui.py` | Shared terminal UI helpers (`rich` panels/tables/spinners and `questionary` arrow-key prompts with text fallback). |
| `tools/setup_wizard.py` | Bilingual (EN/TR) first-run setup CLI that backs up and updates `config.py` and the game XML. |
| `tools/telemetry_check.py` | Standalone CLI listener that waits up to 5 seconds for a valid 264-byte UDP packet. |
| `tools/mock_telemetry.py` | Generates synthetic 264-byte UDP packets at 60 Hz for testing without the game. |
| `tools/theme_selector.py` | Interactive CLI that backs up `settings.py` and writes a selected theme from `dashboards/themes.py`. |
| `install.bat` | Creates `.venv`, installs `requirements.txt`, and launches `tools/setup_wizard.py`. |
| `install.sh` | Creates `.venv` on Linux/Raspberry Pi, installs `requirements.txt` (with optional `--pi` / `--dev` flags), and launches `tools/setup_wizard.py`. |
| `run_dash.bat` | Starts `main.py` inside `.venv`. |
| `run_mock.bat` | Starts `tools/mock_telemetry.py` inside `.venv`. |
| `select_theme.bat` | Starts `tools/theme_selector.py` inside `.venv`. |
| `check_telemetry.bat` | Starts `tools/telemetry_check.py` inside `.venv`. |

## Runtime flow

```text
main.py
  │
  ├─ read config.DASH_STYLE  ("digital" | "analog")
  │
  ├─ import selected dashboard ──► dashboards.digital_dash.run()
  │                            ──► dashboards.analog_dash.run()
  │
  └─ run():
       │
       ├─ init pygame display
       ├─ (Windows) core.overlay_win.apply_overlay()  <- borderless, layered
       ├─ core.UDPListener(config.LISTEN_IP, config.LISTEN_PORT)
       │
       └─ main loop @ 60 FPS:
            │
            ├─ listener.receive()          -> TelemetryData
            ├─ draw RPM bar/needle, speed, gear, pedal bars
            ├─ core.led_controller.update_leds(rpm_ratio)  (if enabled)
            └─ pygame.display.flip()
```

On Windows, `install.bat` creates a Python 3.11, 3.12, or 3.13 virtual environment and runs `tools/setup_wizard.py`. The wizard creates a timestamped backup of `config.py` before writing new values, keeping the existing module interface intact. When DiRT Rally 2.0's `hardware_settings_config.xml` is found, the wizard backs it up and updates its `<udp>` entry as well.

## Data flow

```text
DiRT Rally 2.0  (60 Hz UDP broadcast, Extradata=3)
        │
        ▼
core.udp_listener.py
   - 264-byte packet -> struct.unpack("66f", packet)
   - convert m/s -> km/h, map gear codes, clamp pedal inputs
        │
        ▼
TelemetryData (namedtuple)
   wheel_speed_kmh : int    # average of the four wheel speeds (km/h)
   car_speed_kmh   : int    # longitudinal car speed (km/h)
   rpm             : int    # engine RPM (x10 scaling applied)
   max_rpm         : int    # rev limiter / redline (x10 scaling)
   gear_str        : str    # "N", "R", or "1".."6"
   throttle        : float  # 0.0 .. 1.0 (clamped)
   brake           : float  # 0.0 .. 1.0 (clamped)
        │
        ├─► dashboards/digital_dash.py : RPM bar, speed, gear, pedal bars
        ├─► dashboards/analog_dash.py  : needle, dial ticks, dynamic redline
        └─► core/led_controller.py     : green -> blue -> red shift lights
```

## Platform notes

- **Windows**: When `ENABLE_OVERLAY = True` in `config.py`, `core/overlay_win.py` turns the pygame window into a borderless (`WS_POPUP`), layered (`WS_EX_LAYERED`), click-through (`WS_EX_TRANSPARENT`), always-on-top (`HWND_TOPMOST`) window. `settings.py` supports two transparency modes:
  - `chroma` (default): makes pixels matching `OVERLAY_CHROMA_KEY` (which defaults to `COLOR_BG`) fully transparent via `LWA_COLORKEY`.
  - `alpha`: sets window-wide opacity (`0-255`) via `LWA_ALPHA` using `OVERLAY_ALPHA`.
- **Linux**: Overlay calls only run when `sys.platform == "win32"`. Dashboards open in a standard pygame window.
- **Raspberry Pi (optional)**: When `ENABLE_LEDS = True`, `core/led_controller.py` switches green, blue, and red GPIO LEDs based on `rpm_ratio`.
