# settings.py
# Visual Customization Settings
# Edit these values to change colours, sizes, fonts and overlay position.

# Window dimensions (base resolution)
DIGITAL_WIDTH = 600
DIGITAL_HEIGHT = 200
ANALOG_WIDTH = 600
ANALOG_HEIGHT = 350

# Scale factor: set TARGET_SCALE to resize the dashboard proportionally.
# Set to None to use the base dimensions above without scaling.
# Example: TARGET_SCALE = 1.5 → 600 * 1.5 = 900 px wide; 0.5 → 300 px.
TARGET_SCALE = None  # Set to None to disable scaling

# Overlay window settings (Windows only)
# Position: "bottom-left", "bottom-center", "bottom-right"
OVERLAY_POSITION = "bottom-right"

# Margin from screen edge in pixels (used for left/right positions)
OVERLAY_MARGIN = 20

# Transparency mode: "chroma" (background colour transparent) or "alpha" (semi-transparent window)
OVERLAY_MODE = "chroma"

# Window opacity (0 = fully transparent, 255 = fully opaque). Only used when OVERLAY_MODE == "alpha".
OVERLAY_ALPHA = 220

# Color palette (R, G, B)
COLOR_BG = (25, 25, 30)
COLOR_TEXT_MAIN = (240, 240, 240)
COLOR_TEXT_DIM = (180, 180, 180)
COLOR_TEXT_OUTLINE = (0, 0, 0)
COLOR_RPM_NORMAL = (0, 150, 255)
COLOR_RPM_WARNING = (255, 40, 40)
COLOR_THROTTLE = (40, 220, 100)
COLOR_BRAKE = (255, 60, 60)
COLOR_FRAME = (80, 80, 90)
COLOR_REDLINE = (255, 40, 40, 100)

# Chroma-key colour — pixels matching this colour become transparent in "chroma" mode.
# By default, this dynamically follows COLOR_BG so themes match automatically.
OVERLAY_CHROMA_KEY = COLOR_BG

# RPM warning threshold ratio (0.0 – 1.0) relative to max_rpm.
# Gauge needle or digital bar switches to RPM_WARNING colour when RPM reaches this ratio.
RPM_WARNING_THRESHOLD = 0.90

# Font sizes (base values, scaled automatically when TARGET_SCALE is set)
FONT_HUGE_SIZE = 82
FONT_LARGE_SIZE = 50
FONT_MEDIUM_SIZE = 22
FONT_SMALL_SIZE = 18
FONT_TINY_SIZE = 14

