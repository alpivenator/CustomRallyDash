# Architecture

A custom real-time dashboard for **DiRT Rally 2.0**. The game broadcasts raw
264-byte UDP packets in the **Extradata=3** format at 60 Hz; this project
captures them, decodes the relevant fields, and renders the result either as a
compact **digital dash** or an **analog gauge**, optionally layered as a
click-through overlay on Windows, and optionally mirrored to physical shift
lights on a Raspberry Pi.

## File roles

| Module | Responsibility |
|--------|----------------|
| `main.py` | Unified entry point. Reads `config.DASH_STYLE` and launches the selected dashboard. |
| `config.py` | Central non-visual configuration: listen IP/port, LED enable, overlay enable, style. No code change needed for tuning. |
| `settings.py` | Visual configuration: colors, sizes, fonts, positions. Editable by the user. |
| `udp_listener.py` | Receives 264-byte UDP packets, decodes them with `struct.unpack("66f", …)`, returns a `TelemetryData` namedtuple. |
| `digital_dash.py` | Compact digital dashboard (600×200). RPM bar, gear, speed, pedal bars. Can run as a Windows overlay. |
| `analogdash.py` | Analog gauge dashboard (600×350). Trigonometric needle, dial ticks, dynamic redline, overlay support. |
| `led_controller.py` | Drives physical shift lights on Raspberry Pi GPIO via `gpiozero`. Toggled by `config.ENABLE_LEDS`. |
| `overlay_win.py` | Windows-only Win32 (`ctypes`) helpers: borderless, transparent, click-through overlay window. Supports `alpha` and `chroma` modes. |
| `setup_wizard.py` | First-run CLI setup: backs up and updates `config.py`, then configures the game's UDP telemetry XML. |

## Runtime flow

```
main.py
  │
  ├─ read config.DASH_STYLE  ("digital" | "analog")
  │
  ├─ import the selected dashboard ──► digital_dash.run()
  │                                 ──► analogdash.run()
  │
  └─ run():
       │
       ├─ init pygame display
       ├─ (Windows) overlay_win.apply_overlay()  ← borderless, layered
       ├─ UDPListener(config.LISTEN_IP, config.LISTEN_PORT)
       │
       └─ main loop @ 60 FPS:
            │
            ├─ listener.receive()           → TelemetryData
            ├─ render RPM bar / needle, speed, gear, pedal bars
            ├─ led_controller.update_leds(rpm_ratio)   (if enabled)
            └─ pygame.display.flip()
```

On Windows, `install.bat` creates the Python 3.12 virtual environment and runs
`setup_wizard.py`. The wizard updates the existing `config.py` after creating a
timestamped backup, so the dashboard modules continue to consume the same
configuration interface. It also backs up and updates the game's
`hardwaresettings/hardware_settings_config.xml` file when that file is found.

## Data flow

```
DiRT Rally 2.0  (60 Hz UDP broadcast, Extradata=3)
        │
        ▼
udp_listener.py
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
        ├─► digital_dash.py : RPM bar, speed, gear, pedal bars
        ├─► analogdash.py   : needle, ticks, dynamic redline
        └─► led_controller.py: green → blue → red shift lights
```

## Platform notes

- **Windows** — the dashboards can attach to a Win32 overlay window through
  `overlay_win.py`. The window is borderless (`WS_POPUP`), layered
  (`WS_EX_LAYERED`), click-through (`WS_EX_TRANSPARENT`), and kept on top
  (`HWND_TOPMOST`). Two transparency modes are available:
  - `alpha` — per-pixel alpha via `LWA_ALPHA`; opacity set by `OVERLAY_ALPHA` (0–255).
  - `chroma` — single key color made fully transparent via `LWA_COLORKEY`.
- **Linux** — `overlay_win` is only imported on `sys.platform.startswith("win")`.
  The dashboards run in a normal pygame window.
- **Raspberry Pi (optional)** — `led_controller.py` drives GPIO shift lights
  based on `rpm / max_rpm`.
