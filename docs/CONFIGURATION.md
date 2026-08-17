# Configuration

All settings are plain Python values in two files. Changes take effect the next
time the program is started (there is no hot-reload).

- `config.py` — **system settings** (network, hardware, overlay behaviour).
- `settings.py` — **visual settings** (sizes, colours, fonts, overlay position).

`install.bat` runs `setup_wizard.py`. The setup wizard prompts for language
(English or Turkish). After the setup summary is approved, the wizard creates a
timestamped backup and changes selected system settings directly in `config.py`;
it does not create a second configuration file. Visual settings remain manual.

## System Settings (`config.py`)

| Setting | Default | Description |
|---------|---------|-------------|
| `ENABLE_LEDS` | `False` | Enable Raspberry Pi shift-light LEDs (requires `gpiozero`). |
| `LISTEN_IP` | `"127.0.0.1"` | Network interface for the dashboard UDP listener. Use the dashboard computer's LAN IPv4 address for a remote game computer. |
| `LISTEN_PORT` | `20777` | UDP port the game broadcasts telemetry to. |
| `DASH_STYLE` | `"digital"` | Dashboard variant: `"digital"` or `"analog"`. |
| `ENABLE_OVERLAY` | `True` | Use the borderless, transparent, click-through overlay window (Windows only; silently ignored elsewhere). |
| `OVERLAY_CHROMA_KEY` | `(0, 0, 0)` | Colour made fully transparent in `chroma` mode. |
| `OVERLAY_MODE` | `"alpha"` | Transparency mode: `"alpha"` (semi-transparent window) or `"chroma"` (key colour transparent). |
| `OVERLAY_ALPHA` | `220` | Window opacity in `alpha` mode (`0` = fully transparent, `255` = fully opaque). |

### Network address

By default the program listens only on localhost. Use `127.0.0.1` when the game
and dashboard run on the same computer. For a remote game computer, enter the
dashboard computer's LAN IPv4 address (for example, `192.168.1.25`) in the setup
wizard. The wizard writes that same address to both `config.py` and the game's
telemetry XML.

Existing users with `LISTEN_IP = "0.0.0.0"` are not changed automatically. This
value listens on every interface; replace it with a specific address when you
want to restrict the listener.

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
python telemetry_check.py
```

The tool listens for up to five seconds on `LISTEN_IP` and `LISTEN_PORT`. It
reports the source address when it receives a valid 264-byte packet. It does
not start the dashboard and does not require pygame. If no packet arrives,
check the firewall, the game's XML IP/port values, and that DiRT Rally 2.0 is
running and in a stage. The dashboard must remain closed because both programs
cannot bind the same UDP port at the same time.

## Visual Settings (`settings.py`)

| Setting | Default | Description |
|---------|---------|-------------|
| `DIGITAL_WIDTH` / `DIGITAL_HEIGHT` | `600` / `200` | Base resolution of the digital dashboard. |
| `ANALOG_WIDTH` / `ANALOG_HEIGHT` | `600` / `350` | Base resolution of the analog dashboard. |
| `TARGET_SCALE` | `None` | Proportional scale factor applied to the base resolution. Example: `1.5` → the 600 px wide digital dashboard becomes 900 px; `0.5` shrinks it to 300 px. Set to `None` for no scaling. |
| `OVERLAY_POSITION` | `"bottom-center"` | Overlay position: `"bottom-left"`, `"bottom-center"` or `"bottom-right"` (Windows only). |
| `OVERLAY_MARGIN` | `20` | Distance from the screen edge in pixels (used for left/right positions). |
| `COLOR_BG` | `(25, 25, 30)` | Background colour (RGB 0–255). |
| `COLOR_TEXT_MAIN` | `(240, 240, 240)` | Primary text colour. |
| `COLOR_TEXT_DIM` | `(180, 180, 180)` | Dimmed/secondary text colour. |
| `COLOR_RPM_NORMAL` | `(0, 150, 255)` | RPM bar/needle colour below the redline. |
| `COLOR_RPM_WARNING` | `(255, 40, 40)` | RPM colour at/above the redline. |
| `COLOR_THROTTLE` | `(40, 220, 100)` | Throttle bar colour. |
| `COLOR_BRAKE` | `(255, 60, 60)` | Brake bar colour. |
| `COLOR_FRAME` | `(80, 80, 90)` | Frame/outline colour. |
| `COLOR_REDLINE` | `(255, 40, 40, 100)` | Redline marker; the 4th value is alpha (`100` = semi-transparent red). |
| `FONT_HUGE_SIZE` | `80` | Largest font (main values). |
| `FONT_LARGE_SIZE` | `48` | Large font (labels). |
| `FONT_MEDIUM_SIZE` | `20` | Medium font (digital dashboard only). |
| `FONT_SMALL_SIZE` | `18` | Small font. |
| `FONT_TINY_SIZE` | `14` | Tiny font. |

Font sizes are scaled automatically when `TARGET_SCALE` is set.

## Security Notes

The telemetry stream is unauthenticated UDP broadcast on the local network.
Only run the program on networks you trust. Set `LISTEN_IP` to the machine's
LAN IP instead of `0.0.0.0` if you want to restrict which interface receives
packets.
