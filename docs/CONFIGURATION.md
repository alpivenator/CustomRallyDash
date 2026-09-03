# Configuration Reference — CustomRallyDash

[Türkçe](CONFIGURATION_TR.md) | **English**

CustomRallyDash uses standard Python files for straightforward configuration without external parser overhead. Changes take effect the next time you start the application (no hot-reload).

- **`config.py`** — Runtime & hardware settings (network, dashboard style, Windows overlay toggle, Raspberry Pi LEDs).
- **`settings.py`** — Visual styling (dimensions, scale, colors, fonts, overlay positioning & transparency).

> **Tip**: You rarely need to edit code manually. First-time setup can be done with `install.bat` (or `python tools/setup_wizard.py`), and visual themes can be swapped with `select_theme.bat` (or `python tools/theme_selector.py`).

---

## Quick Configuration (Most Common Settings)

Most users only ever need to configure these core options:

| Goal | File | Setting | Default / Recommended |
| :--- | :--- | :--- | :--- |
| **Switch HUD style** | `config.py` | `DASH_STYLE` | `"digital"` (horizontal bar HUD) or `"analog"` (circular gauge) |
| **Scale dashboard size** | `settings.py` | `TARGET_SCALE` | `None` (native size), `1.25` (+25%), `0.8` (-20%) |
| **Toggle Windows overlay** | `config.py` | `ENABLE_OVERLAY` | `True` (transparent click-through overlay on Windows) |
| **Change overlay position** | `settings.py` | `OVERLAY_POSITION` | `"bottom-right"`, `"bottom-center"`, or `"bottom-left"` |
| **Switch color theme** | `settings.py` | *(Automated)* | Run `select_theme.bat` to apply motorsport presets |
| **Telemetry IP address** | `config.py` | `LISTEN_IP` | `"127.0.0.1"` (same PC) or dashboard LAN IP (multi-machine) |

---

## Game Setup (DiRT Rally 2.0 Telemetry)

To enable 60 Hz UDP telemetry output in DiRT Rally 2.0, edit the game configuration file:

```text
Documents\My Games\DiRT Rally 2.0\hardwaresettings\hardware_settings_config.xml
```

Locate the `<motion_platform>` section and verify/update the `<udp>` tag:

```xml
<udp enabled="true" extradata="3" ip="127.0.0.1" port="20777" delay="1" />
```

- **Single PC**: Set `ip="127.0.0.1"`.
- **Dual PC / Raspberry Pi**: Set `ip` to the local LAN IPv4 address of the computer running CustomRallyDash (e.g., `192.168.1.50`).

> **Important for Overlay Users**: Set the game's display mode to **Borderless Windowed** or **Windowed** in DiRT Rally 2.0 graphics settings so the dashboard overlay stays on top.

---

## Testing & Verification Tools

Run these scripts from the project root without modifying any files:

- **Connection Test**: Run `check_telemetry.bat` (or `python tools/telemetry_check.py`). Verifies if active 264-byte UDP packets are arriving from the game.
- **Offline Preview**: Run `python main.py --mock` (or launch `run_mock.bat` and `run_dash.bat`). Generates realistic synthetic WRC telemetry without needing the game running.
- **Theme Switcher**: Run `select_theme.bat` (or `python tools/theme_selector.py`). Interactively updates `settings.py` with presets like *Subaru WRC*, *GT3 Racing*, or *Night Neon*.

---

## Detailed System Settings (`config.py`)

| Setting | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `DASH_STYLE` | `str` | `"digital"` | Dashboard variant: `"digital"` (600×200 px bar HUD) or `"analog"` (600×350 px circular tachometer). |
| `LISTEN_IP` | `str` | `"127.0.0.1"` | Interface to bind UDP socket. Use `"127.0.0.1"` for local play, or LAN IP / `"0.0.0.0"` for remote. |
| `LISTEN_PORT` | `int` | `20777` | UDP port matching the port defined in the game XML. |
| `ENABLE_OVERLAY` | `bool` | `True` | Enables borderless transparent click-through window (Windows only; ignored on Linux). |
| `ENABLE_LEDS` | `bool` | `False` | Enables physical shift-light GPIO LEDs on Raspberry Pi (requires `gpiozero`). |

---

## Detailed Visual & Overlay Settings (`settings.py`)

### Display & Overlay Positioning

| Setting | Default | Description |
| :--- | :--- | :--- |
| `TARGET_SCALE` | `None` | Proportional scaling multiplier (e.g. `1.5` increases digital HUD from 600×200 to 900×300 px; fonts scale automatically). `None` retains default resolution. |
| `DIGITAL_WIDTH` / `HEIGHT` | `600` / `200` | Native resolution of digital HUD. |
| `ANALOG_WIDTH` / `HEIGHT` | `600` / `350` | Native resolution of analog tachometer. |
| `OVERLAY_POSITION` | `"bottom-right"` | Screen placement on Windows: `"bottom-right"`, `"bottom-center"`, `"bottom-left"`. |
| `OVERLAY_MARGIN` | `20` | Distance in pixels from screen edges. |
| `OVERLAY_MODE` | `"chroma"` | Window compositing mode: `"chroma"` (background is made 100% transparent HUD) or `"alpha"` (semi-transparent panel). |
| `OVERLAY_ALPHA` | `220` | Window opacity when `OVERLAY_MODE = "alpha"` (`0` = invisible, `255` = solid). |
| `OVERLAY_CHROMA_KEY` | `COLOR_BG` | Color made transparent in `"chroma"` mode. Defaults dynamically to `COLOR_BG`. |

### Colors & Redline

| Setting | Default | Description |
| :--- | :--- | :--- |
| `RPM_WARNING_THRESHOLD` | `0.90` | Fraction of engine redline (0.0–1.0) where warning colors/flash trigger. |
| `COLOR_BG` | `(25, 25, 30)` | Background color (RGB). |
| `COLOR_RPM_NORMAL` | `(0, 150, 255)` | RPM bar / needle color during normal operation. |
| `COLOR_RPM_WARNING` | `(255, 40, 40)` | RPM bar / needle color when approaching or exceeding redline. |
| `COLOR_THROTTLE` | `(40, 220, 100)` | Throttle pedal indicator color. |
| `COLOR_BRAKE` | `(255, 60, 60)` | Brake pedal indicator color. |
| `COLOR_TEXT_MAIN` | `(240, 240, 240)` | Primary high-contrast text color. |
| `COLOR_TEXT_DIM` | `(180, 180, 180)` | Secondary / dimmed label text color. |
| `COLOR_TEXT_OUTLINE` | `(0, 0, 0)` | Drop-shadow / contrast outline around text. |
| `COLOR_FRAME` | `(80, 80, 90)` | Borders, divider lines, and gauge bezels. |
| `COLOR_REDLINE` | `(255, 65, 105, 110)` | RGBA redline marker on analog gauge (4th value is alpha opacity). |

### Typography (Base Font Sizes in Pixels)

Font sizes are automatically multiplied by `TARGET_SCALE`:

| Setting | Default | Used For |
| :--- | :--- | :--- |
| `FONT_HUGE_SIZE` | `82` | Gear indicator readout |
| `FONT_LARGE_SIZE` | `50` | Primary speed readout (km/h) |
| `FONT_MEDIUM_SIZE` | `22` | RPM numerical readout in digital HUD |
| `FONT_SMALL_SIZE` | `18` | Auxiliary telemetry labels (KM/H, RPM, Gear labels) |
| `FONT_TINY_SIZE` | `14` | Dial numbers and pedal bar labels (THR / BRK) |

---

## Security & Network Notes

The telemetry stream is unauthenticated UDP broadcast on the local network. Only run the program on trusted networks. If multiple network adapters are present, specify the exact machine IPv4 address in `LISTEN_IP` rather than `0.0.0.0` to restrict UDP listening.
