# Configuration

All settings are plain Python values in two files. Changes take effect the next
time the program is started (there is no hot-reload).

- `config.py` — **system settings** (network, hardware, overlay behaviour).
- `settings.py` — **visual settings** (sizes, colours, fonts, overlay position).

## System Settings (`config.py`)

| Setting | Default | Description |
|---------|---------|-------------|
| `ENABLE_LEDS` | `False` | Enable Raspberry Pi shift-light LEDs (requires `gpiozero`). |
| `LISTEN_IP` | `"0.0.0.0"` | Network interface to listen on. See *Why `0.0.0.0`?* below. |
| `LISTEN_PORT` | `20777` | UDP port the game broadcasts telemetry to. |
| `DASH_STYLE` | `"digital"` | Dashboard variant: `"digital"` or `"analog"`. |
| `ENABLE_OVERLAY` | `True` | Use the borderless, transparent, click-through overlay window (Windows only; silently ignored elsewhere). |
| `OVERLAY_CHROMA_KEY` | `(0, 0, 0)` | Colour made fully transparent in `chroma` mode. |
| `OVERLAY_MODE` | `"alpha"` | Transparency mode: `"alpha"` (semi-transparent window) or `"chroma"` (key colour transparent). |
| `OVERLAY_ALPHA` | `220` | Window opacity in `alpha` mode (`0` = fully transparent, `255` = fully opaque). |

### Why `LISTEN_IP = "0.0.0.0"`?

By default the program listens on all network interfaces. There are two reasons:

1. If the game runs on a different computer, the dashboard must be able to
   receive packets from that machine.
2. On Windows, using `127.0.0.1` (localhost) can cause the Windows Firewall to
   block loopback UDP traffic. With `0.0.0.0`, all interfaces are listened to,
   and it is enough to set the `ip` address in the game's
   `hardware_settings_config.xml` to the computer's local network IP
   (`192.168.x.x`) — the firewall does not interfere with that traffic.

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
Only run the program on networks you trust, and set `LISTEN_IP` to the
machine's LAN IP instead of `0.0.0.0` if you want to restrict which interface
receives packets.
