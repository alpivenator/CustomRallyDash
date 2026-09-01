# config.py
# System Configuration Settings
# Edit these values to customise behaviour without changing application code.
# The setup wizard can update the selected values after creating a backup.

# ----------------------------------------------------------------------
# Hardware
# ----------------------------------------------------------------------
# Set to True when running on a Raspberry Pi with physical shift-light LEDs.
ENABLE_LEDS = False

# ----------------------------------------------------------------------
# Network
# ----------------------------------------------------------------------
# Address and port used by the dashboard's UDP listener.
# The setup wizard can change this to the dashboard computer's LAN address
# when the game runs on another computer.
LISTEN_IP = "127.0.0.1"
LISTEN_PORT = 20777

# ----------------------------------------------------------------------
# Dashboard Style
# ----------------------------------------------------------------------
# "digital"  — compact horizontal bar dashboard (600 x 200 px)
# "analog"   — circular-needle gauge dashboard (600 x 350 px)
DASH_STYLE = "analog"

# ----------------------------------------------------------------------
# Overlay Toggle (Windows only)
# ----------------------------------------------------------------------
# Enable a borderless, transparent, click-through window that stays
# on top of the game. Only functional on Windows; silently ignored
# elsewhere. Visual and positioning settings are located in settings.py.
ENABLE_OVERLAY = True

