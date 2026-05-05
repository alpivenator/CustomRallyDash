# config.py
# System Configuration Settings
# Set to True if running on Raspberry Pi with LEDs connected.
# Set to False if running on the main PC or without hardware.
ENABLE_LEDS = False

# Network Settings
LISTEN_IP = "0.0.0.0"
LISTEN_PORT = 20777

# ----------------------------------------------------------------------
# Overlay Settings (borderless, transparent, click-through window)
# ----------------------------------------------------------------------
# Set to True to enable overlay on Windows.  Has no effect on other
# platforms or if overlay_win module is missing.
ENABLE_OVERLAY = False

# Colour used for chroma-key transparency.  Pixels of this exact colour
# in the dashboard window will become fully transparent.
OVERLAY_CHROMA_KEY = (0, 0, 0)  # R, G, B

# If True, the overlay window is placed at the bottom-centre of the primary
# monitor.  Only relevant when ENABLE_OVERLAY is True.
OVERLAY_BOTTOM_CENTER = True
