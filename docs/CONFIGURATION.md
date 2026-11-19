# Configuration Reference: CustomRallyDash

[Türkçe](CONFIGURATION_TR.md) | **English**

CustomRallyDash reads its configuration directly from two Python files. Changes take effect the next time you start the application (there is no hot-reload).

- `config.py`: Runtime and hardware settings (network, dashboard style, Windows overlay toggle, Raspberry Pi LEDs).
- `settings.py`: Visual styling (dimensions, scale, colors, fonts, overlay position, and transparency).

You rarely need to edit these files by hand. For first-time setup, run `install.bat` on Windows, `./install.sh` on Linux/Raspberry Pi, or `python tools/setup_wizard.py` directly. To switch color themes, run `select_theme.bat` or `python tools/theme_selector.py`.

## Quick configuration

Most users only need to adjust the options below:

| Goal | File | Setting | Default / options |
| :--- | :--- | :--- | :--- |
| Switch HUD style | `config.py` | `DASH_STYLE` | `"digital"` (horizontal bar HUD) or `"analog"` (circular gauge) |
| Scale dashboard size | `settings.py` | `TARGET_SCALE` | `None` (native size), `1.25` (+25%), `0.8` (-20%) |
| Toggle Windows overlay | `config.py` | `ENABLE_OVERLAY` | `True` (borderless click-through overlay on Windows) |
| Change overlay position | `settings.py` | `OVERLAY_POSITION` | `"bottom-right"`, `"bottom-center"`, or `"bottom-left"` |
| Switch color theme | `settings.py` | *(via CLI)* | Run `select_theme.bat` or `python tools/theme_selector.py` to apply presets |
| Telemetry IP address | `config.py` | `LISTEN_IP` | `"127.0.0.1"` (same PC) or dashboard LAN IP (separate device) |

## Game setup (DiRT Rally 2.0)

To enable 60 Hz UDP telemetry in DiRT Rally 2.0, open the game's hardware config file:

```text
Documents\My Games\DiRT Rally 2.0\hardwaresettings\hardware_settings_config.xml
```

Find `<motion_platform>` and add or update the `<udp>` tag:

```xml
<udp enabled="true" extradata="3" ip="127.0.0.1" port="20777" delay="1" />
```

- Single PC: keep `ip="127.0.0.1"`.
- Separate PC or Raspberry Pi: set `ip` to the local LAN IPv4 address of the device running CustomRallyDash (for example, `192.168.1.50`).

If you use the Windows overlay, set DiRT Rally 2.0's video mode to **Windowed** or **Borderless Windowed** so the overlay stays visible on top of the game.

## Testing and verification tools

Run these scripts from the project root:

- Connection test: Run `check_telemetry.bat` (or `python tools/telemetry_check.py`) to listen for incoming 264-byte UDP packets from the game.
- Offline preview: Run `python main.py --mock`, or launch `run_mock.bat` together with `run_dash.bat`. Both send simulated 60 Hz WRC acceleration and braking telemetry without the game running.
- Theme switcher: Run `select_theme.bat` (or `python tools/theme_selector.py`) to write presets such as `Subaru Classic WRC`, `GT3 Competition`, or `Night Stage Neon (Cyberpunk)` to `settings.py`.

## System settings (`config.py`)

| Setting | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `DASH_STYLE` | `str` | `"digital"` | Dashboard layout: `"digital"` (600x200 px bar HUD) or `"analog"` (600x350 px circular tachometer). |
| `LISTEN_IP` | `str` | `"127.0.0.1"` | Network interface for the UDP socket. Use `"127.0.0.1"` for local play, or a LAN IP / `"0.0.0.0"` for remote telemetry. |
| `LISTEN_PORT` | `int` | `20777` | UDP listening port; must match `port` in the game XML. |
| `ENABLE_OVERLAY` | `bool` | `True` | Enables the borderless, transparent, click-through overlay (Windows only; ignored on Linux). |
| `ENABLE_LEDS` | `bool` | `False` | Enables physical GPIO shift lights on Raspberry Pi (requires `gpiozero`). |

## Visual and overlay settings (`settings.py`)

### Display and overlay placement

| Setting | Default | Description |
| :--- | :--- | :--- |
| `TARGET_SCALE` | `None` | Proportional multiplier (for example, `1.5` scales the digital HUD from 600x200 to 900x300 px and scales fonts along with it). `None` keeps base dimensions. |
| `DIGITAL_WIDTH` / `HEIGHT` | `600` / `200` | Base resolution of the digital HUD in pixels. |
| `ANALOG_WIDTH` / `HEIGHT` | `600` / `350` | Base resolution of the analog tachometer in pixels. |
| `OVERLAY_POSITION` | `"bottom-right"` | Placement on Windows: `"bottom-right"`, `"bottom-center"`, or `"bottom-left"`. |
| `OVERLAY_MARGIN` | `20` | Pixel margin from the left or right screen edge. |
| `OVERLAY_MODE` | `"chroma"` | Transparency mode: `"chroma"` (makes the background color fully transparent) or `"alpha"` (semi-transparent window). |
| `OVERLAY_ALPHA` | `220` | Window opacity when `OVERLAY_MODE = "alpha"` (`0` = invisible, `255` = opaque). |
| `OVERLAY_CHROMA_KEY` | `COLOR_BG` | Color treated as transparent in `"chroma"` mode. Follows `COLOR_BG` by default. |

### Colors and redline threshold

| Setting | Default | Description |
| :--- | :--- | :--- |
| `RPM_WARNING_THRESHOLD` | `0.90` | Fraction of `max_rpm` (`0.0-1.0`) where the RPM bar or needle switches to the warning color. |
| `COLOR_BG` | `(25, 25, 30)` | Background color (RGB). |
| `COLOR_RPM_NORMAL` | `(0, 150, 255)` | RPM bar and needle color below the warning threshold. |
| `COLOR_RPM_WARNING` | `(255, 40, 40)` | RPM bar and needle color at or above the warning threshold. |
| `COLOR_THROTTLE` | `(40, 220, 100)` | Throttle pedal bar color. |
| `COLOR_BRAKE` | `(255, 60, 60)` | Brake pedal bar color. |
| `COLOR_TEXT_MAIN` | `(240, 240, 240)` | Primary text color. |
| `COLOR_TEXT_DIM` | `(180, 180, 180)` | Secondary label color. |
| `COLOR_TEXT_OUTLINE` | `(0, 0, 0)` | Dark outline around text for contrast on bright stages. |
| `COLOR_FRAME` | `(80, 80, 90)` | Borders, gauge ring, and bar outlines. |
| `COLOR_REDLINE` | `(255, 65, 105, 110)` | RGBA redline sector color on the analog gauge (fourth value sets alpha). |

### Font sizes

All base font sizes are in pixels and scale with `TARGET_SCALE`:

| Setting | Default | Used for |
| :--- | :--- | :--- |
| `FONT_HUGE_SIZE` | `82` | Gear indicator |
| `FONT_LARGE_SIZE` | `50` | Speed readout (`km/h`) |
| `FONT_MEDIUM_SIZE` | `22` | Numeric RPM readout in the digital HUD |
| `FONT_SMALL_SIZE` | `18` | `SPEED` and `GEAR` labels in digital HUD; `KM/H`, `THR`, and `BRK` labels in analog gauge |
| `FONT_TINY_SIZE` | `14` | `THR` and `BRK` labels in digital HUD; dial numbers on the analog gauge |

## Network and security notes

DiRT Rally 2.0 broadcasts UDP telemetry over the local network without encryption or authentication. Run the listener only on trusted networks. On machines with multiple network adapters, set `LISTEN_IP` to the specific LAN IPv4 address instead of `"0.0.0.0"` to limit which interface accepts packets.
