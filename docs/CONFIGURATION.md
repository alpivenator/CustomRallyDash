# Configuration Reference — CustomRallyDash

All settings are plain Python values in two files. Changes take effect the next
time the program is started (there is no hot-reload).

- `config.py` — **system settings** (network, hardware, overlay behaviour).
- `settings.py` — **visual settings** (sizes, colours, fonts, overlay position).

`install.bat` runs `tools/setup_wizard.py`. If you downloaded the repository
as a ZIP file on Windows, make sure to unblock the archive (Right Click ->
Properties -> check Unblock) before extracting and
running batch files. The setup wizard prompts for language (English or Turkish).
After the setup summary is approved, the wizard creates a timestamped backup
and changes selected system settings directly in `config.py`; it does not
create a second configuration file. Visual settings remain manual.

## System Settings (`config.py`)

| Setting | Default | Description |
|---------|---------|-------------|
| `ENABLE_LEDS` | `False` | Enable Raspberry Pi shift-light LEDs (requires `gpiozero`). |
| `LISTEN_IP` | `"127.0.0.1"` | Network interface for the dashboard UDP listener. Use the dashboard computer's LAN IPv4 address for a remote game computer. |
| `LISTEN_PORT` | `20777` | UDP port the game broadcasts telemetry to. |
| `DASH_STYLE` | `"digital"` | Dashboard variant: `"digital"` (compact horizontal HUD, default) or `"analog"` (circular gauge). |
| `ENABLE_OVERLAY` | `True` | Enable the borderless, transparent, click-through overlay window (Windows only; silently ignored elsewhere). |


### Dashboard style

`DASH_STYLE` in `config.py` selects the active display layout:
- `"digital"` (**Default / Recommended**): Compact horizontal bar HUD (600×200 px) designed for high-visibility stage awareness and transparent in-game overlay placement.
- `"analog"`: Circular tachometer gauge (600×350 px) with needle, dial markings, dynamic redline zone, and central gear readout.


### Network address

By default the program listens only on localhost. Use `127.0.0.1` when the game
and dashboard run on the same computer. For a remote game computer, enter the
dashboard computer's LAN IPv4 address (for example, `192.168.1.25`) in the setup
wizard. The wizard writes that same address to both `config.py` and the game's
telemetry XML.

### Game telemetry configuration

The game file is normally located at:

```text
Documents\My Games\DiRT Rally 2.0\hardwaresettings\hardware_settings_config.xml
```

Inside the `<motion_platform>` section, enable the UDP telemetry entry:

```xml
<udp enabled="true" extradata="3" ip="127.0.0.1" port="20777" delay="1" />
```

The `ip` value is the dashboard computer's address. Use `127.0.0.1` when both
programs run on the same computer; for a remote game computer, use the
dashboard computer's LAN IPv4 address. The setup wizard asks for this address
and creates a backup only after you approve the summary.

### Connection check

After setup, ensure the dashboard is closed and run the diagnostic tool. On Windows:

```sh
check_telemetry.bat
```

Or run via Python in your active virtual environment:

```sh
python tools/telemetry_check.py
```

The tool listens for up to five seconds on `LISTEN_IP` and `LISTEN_PORT`. It
reports the source address when it receives a valid 264-byte packet. It does
not start the dashboard and does not require pygame. If no packet arrives,
check the firewall, the game's XML IP/port values, and that DiRT Rally 2.0 is
running and in a stage. The dashboard must remain closed because both programs
cannot bind the same UDP port at the same time.

### Offline preview with mock telemetry

To test or preview dashboard styles without running DiRT Rally 2.0:

On Windows:
```sh
run_mock.bat
```
Keep this broadcaster window open, and double-click `run_dash.bat`.

Alternatively, launch both together:
```sh
python main.py --mock
```

### Visual theme customization

To switch between motorsport-inspired colour presets safely without editing `settings.py` by hand:

On Windows:
```sh
select_theme.bat
```

Or run via Python in your active virtual environment:
```sh
python tools/theme_selector.py
```

## Visual & Overlay Settings (`settings.py`)

| Setting | Default | Description |
|---------|---------|-------------|
| `DIGITAL_WIDTH` / `DIGITAL_HEIGHT` | `600` / `200` | Base resolution of the digital dashboard. |
| `ANALOG_WIDTH` / `ANALOG_HEIGHT` | `600` / `350` | Base resolution of the analog dashboard. |
| `TARGET_SCALE` | `None` | Proportional scale factor applied to the base resolution. Example: `1.5` → the 600 px wide digital dashboard becomes 900 px; `0.5` shrinks it to 300 px. Set to `None` for no scaling. |
| `OVERLAY_POSITION` | `"bottom-right"` | Overlay position on display: `"bottom-left"`, `"bottom-center"` or `"bottom-right"` (Windows only). |
| `OVERLAY_MARGIN` | `20` | Distance from screen edge in pixels (used for left/right positions). |
| `OVERLAY_MODE` | `"chroma"` | Transparency mode: `"chroma"` (background colour transparent HUD) or `"alpha"` (semi-transparent window). |
| `OVERLAY_ALPHA` | `220` | Window opacity in `alpha` mode (`0` = fully transparent, `255` = fully opaque). |
| `OVERLAY_CHROMA_KEY` | `COLOR_BG` | Colour made fully transparent in `chroma` mode. By default points dynamically to `COLOR_BG`. |
| `COLOR_BG` | `(25, 25, 30)` | Background colour (RGB 0–255). |
| `COLOR_TEXT_MAIN` | `(240, 240, 240)` | Primary text colour. |
| `COLOR_TEXT_DIM` | `(180, 180, 180)` | Dimmed/secondary text colour. |
| `COLOR_TEXT_OUTLINE` | `(0, 0, 0)` | Contrast outline colour rendered around text for high readability. |
| `COLOR_RPM_NORMAL` | `(0, 150, 255)` | RPM bar/needle colour below the redline. |
| `COLOR_RPM_WARNING` | `(255, 40, 40)` | RPM colour at/above the redline. |
| `COLOR_THROTTLE` | `(40, 220, 100)` | Throttle bar colour. |
| `COLOR_BRAKE` | `(255, 60, 60)` | Brake bar colour. |
| `COLOR_FRAME` | `(80, 80, 90)` | Frame/outline colour. |
| `COLOR_REDLINE` | `(255, 65, 105, 110)` | Redline marker; the 4th value is alpha (`110` = semi-transparent rose-red). |
| `RPM_WARNING_THRESHOLD` | `0.90` | Fraction of `max_rpm` (0.0–1.0) at which the needle / RPM bar turns red. |
| `FONT_HUGE_SIZE` | `82` | Largest font (gear value). |
| `FONT_LARGE_SIZE` | `50` | Large font (speed values). |
| `FONT_MEDIUM_SIZE` | `22` | Medium font (RPM text in digital dashboard). |
| `FONT_SMALL_SIZE` | `18` | Small font (labels). |
| `FONT_TINY_SIZE` | `14` | Tiny font (markings / pedal labels). |

Font sizes are scaled automatically when `TARGET_SCALE` is set.


## Security Notes

The telemetry stream is unauthenticated UDP broadcast on the local network.
Only run the program on networks you trust. Set `LISTEN_IP` to the machine's
LAN IP if you want to restrict which interface receives
packets.
