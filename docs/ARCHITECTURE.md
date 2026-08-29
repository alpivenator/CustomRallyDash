# Architecture

A custom real-time dashboard for **DiRT Rally 2.0**. The game broadcasts raw
264-byte UDP packets in the **Extradata=3** format at 60 Hz; this project
captures them, decodes the relevant fields, and renders the result either as a
compact **digital dash** or an **analog gauge**, optionally layered as a
click-through overlay on Windows, and optionally mirrored to physical shift
lights on a Raspberry Pi.

## Directory Structure & File Roles

```
ralli-codex/
├── .github/
│   ├── workflows/
│   │   └── ci.yml            # Automated GitHub Actions CI (ruff + pytest)
│   └── ISSUE_TEMPLATE/       # GitHub issue report and feature request templates
├── core/
│   ├── __init__.py           # Package exports for telemetry and platform helpers
│   ├── udp_listener.py       # UDP socket listener & Extradata=3 packet decoder
│   ├── overlay_win.py        # Windows Win32 ctypes overlay helpers
│   └── led_controller.py     # Raspberry Pi GPIO shift-light driver (gpiozero)
├── dashboards/
│   ├── __init__.py           # Package exports for dashboard runners
│   ├── digital_dash.py       # Compact digital dashboard (600×200 px)
│   ├── analog_dash.py        # Analog gauge dashboard (600×350 px)
│   └── themes.py             # Motorsport and simulator colour theme presets
├── tools/
│   ├── __init__.py           # Package exports for setup and check utilities
│   ├── setup_wizard.py       # Bilingual first-run CLI setup wizard
│   ├── telemetry_check.py    # UDP connectivity diagnostic tool
│   ├── mock_telemetry.py     # 60 Hz synthetic UDP packet generator
│   └── theme_selector.py     # Standalone CLI theme switcher
├── docs/                     # Architecture, configuration, roadmap, and changelog docs
│   ├── ARCHITECTURE.md       # Technical design and architecture reference
│   ├── CONFIGURATION.md      # Configuration options and hardware setup
│   ├── CHANGELOG.md          # Version history (English)
│   ├── CHANGELOG_TR.md       # Version history (Turkish)
│   ├── ROADMAP.md            # Planned milestones (English)
│   └── ROADMAP_TR.md         # Planned milestones (Turkish)
├── tests/                    # Unit tests (pytest)
├── main.py                   # Unified application entry point (supports --mock)
├── config.py                 # Central system/hardware configuration
├── settings.py               # Visual layout & styling configuration
├── install.bat               # Windows environment setup & wizard launcher
├── run_dash.bat              # Windows dashboard launcher
├── run_mock.bat              # Windows mock telemetry launcher
├── select_theme.bat          # Windows theme selector launcher
└── check_telemetry.bat       # Windows telemetry check launcher
```

| Module / File | Responsibility |
|---------------|----------------|
| `main.py` | Unified entry point. Reads `config.DASH_STYLE` and launches dashboard. Supports `--mock` for automatic preview. |
| `config.py` | Central non-visual configuration: listen IP/port, LED enable, overlay enable, style. Editable by user & setup wizard. |
| `settings.py` | Visual configuration: colors, sizes, fonts, positions. Editable by user & theme selector. |
| `core/udp_listener.py` | Receives 264-byte UDP packets, decodes with `struct.unpack("66f", …)`, returns `TelemetryData`. |
| `core/overlay_win.py` | Windows Win32 (`ctypes`) helpers: borderless, transparent, click-through overlay window. |
| `core/led_controller.py` | Drives physical shift lights on Raspberry Pi GPIO via `gpiozero`. Toggled by `config.ENABLE_LEDS`. |
| `dashboards/digital_dash.py` | Compact digital dashboard (600×200). RPM bar, gear, speed, pedal bars. |
| `dashboards/analog_dash.py` | Analog gauge dashboard (600×350). Trigonometric needle, dial ticks, dynamic redline, central gear housing. |
| `dashboards/themes.py` | Curated motorsport colour presets (`modern_dark`, `subaru_classic`, `gt3_racing`, `night_neon`, `retro_amber`). |
| `tools/setup_wizard.py` | First-run CLI setup with English and Turkish language support. |
| `tools/telemetry_check.py` | Dependency-free CLI diagnostic that waits for valid telemetry packets. |
| `tools/mock_telemetry.py` | Generates synthetic 264-byte UDP packets at 60 Hz for live preview without running the game. |
| `tools/theme_selector.py` | Interactive CLI to select and apply curated colour presets to `settings.py`. |
| `run_mock.bat` | Windows batch launcher for standalone mock telemetry broadcaster. |
| `select_theme.bat` | Windows batch launcher for theme selector. |
| `check_telemetry.bat` | Windows batch launcher for telemetry connectivity diagnostic. |


## Runtime flow

```
main.py
  │
  ├─ read config.DASH_STYLE  ("digital" | "analog")
  │
  ├─ import the selected dashboard ──► dashboards.digital_dash.run()
  │                                 ──► dashboards.analog_dash.run()
  │
  └─ run():
       │
       ├─ init pygame display
       ├─ (Windows) core.overlay_win.apply_overlay()  ← borderless, layered
       ├─ core.UDPListener(config.LISTEN_IP, config.LISTEN_PORT)
       │
       └─ main loop @ 60 FPS:
            │
            ├─ listener.receive()           → TelemetryData
            ├─ render RPM bar / needle, speed, gear, pedal bars
            ├─ core.led_controller.update_leds(rpm_ratio)   (if enabled)
            └─ pygame.display.flip()
```

On Windows, `install.bat` creates the Python 3.12 virtual environment and runs
`tools/setup_wizard.py`. The wizard presents a bilingual interface (English / Turkish)
and updates the existing `config.py` after creating a timestamped backup, so the
dashboard modules continue to consume the same configuration interface. It also
backs up and updates the game's `hardwaresettings/hardware_settings_config.xml`
file when that file is found.

## Data flow

```
DiRT Rally 2.0  (60 Hz UDP broadcast, Extradata=3)
        │
        ▼
core.udp_listener.py
   - 264-byte packet → struct.unpack("66f", packet)
   - convert m/s → km/h, decode gear, clamp pedals
        │
        ▼
TelemetryData (namedtuple)
   wheel_speed_kmh : int    # average of the four wheel speeds (km/h)
   car_speed_kmh   : int    # car longitudinal speed (km/h)
   rpm             : int    # engine RPM (×10 scaling already applied)
   max_rpm         : int    # rev limiter / redline (×10 scaling)
   gear_str        : str    # "N", "R", or "1".."6"
   throttle        : float  # 0.0 .. 1.0 (clamped)
   brake           : float  # 0.0 .. 1.0 (clamped)
        │
        ├─► dashboards/digital_dash.py : RPM bar, speed, gear, pedal bars
        ├─► dashboards/analog_dash.py  : needle, ticks, dynamic redline
        └─► core/led_controller.py     : green → blue → red shift lights
```

## Platform notes

- **Windows** — the dashboards can attach to a Win32 overlay window through
  `core/overlay_win.py`. The window is borderless (`WS_POPUP`), layered
  (`WS_EX_LAYERED`), click-through (`WS_EX_TRANSPARENT`), and kept on top
  (`HWND_TOPMOST`). Two transparency modes are available:
  - `alpha` — per-pixel alpha via `LWA_ALPHA`; opacity set by `OVERLAY_ALPHA` (0–255).
  - `chroma` — single key color made fully transparent via `LWA_COLORKEY`.
- **Linux** — `overlay_win` is only imported on `sys.platform.startswith("win")`.
  The dashboards run in a normal pygame window.
- **Raspberry Pi (optional)** — `core/led_controller.py` drives GPIO shift lights
  based on `rpm / max_rpm`.
