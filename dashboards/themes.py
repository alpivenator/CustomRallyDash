# dashboards/themes.py
# DiRT Rally 2.0 — Curated Motorsport & Simulator Colour Themes
#
# Clean, high-contrast colour palettes inspired by motorsport heritage,
# modern GT3 cockpits, and OLED high-visibility telemetry gauges.

from typing import Any

THEMES: dict[str, dict[str, Any]] = {
    "modern_dark": {
        "name": "Modern Dark (Default)",
        "description": "Sleek dark grey cockpit with high-visibility cyan/blue RPM and red rev limiter.",
        "colors": {
            "COLOR_BG": (25, 25, 30),
            "COLOR_TEXT_MAIN": (240, 240, 240),
            "COLOR_TEXT_DIM": (180, 180, 180),
            "COLOR_RPM_NORMAL": (0, 150, 255),
            "COLOR_RPM_WARNING": (255, 40, 40),
            "COLOR_THROTTLE": (40, 220, 100),
            "COLOR_BRAKE": (255, 60, 60),
            "COLOR_FRAME": (80, 80, 90),
            "COLOR_REDLINE": (255, 40, 40, 100),
        },
    },
    "subaru_classic": {
        "name": "Subaru Classic WRC",
        "description": "Iconic World Rally Championship 555 heritage: World Rally Blue, Gold/Yellow accents, and STi Cherry Red alerts.",
        "colors": {
            "COLOR_BG": (12, 18, 32),
            "COLOR_TEXT_MAIN": (245, 245, 250),
            "COLOR_TEXT_DIM": (140, 160, 190),
            "COLOR_RPM_NORMAL": (255, 204, 0),  # Rally Gold
            "COLOR_RPM_WARNING": (255, 30, 85),  # STi Pink/Red
            "COLOR_THROTTLE": (50, 215, 120),
            "COLOR_BRAKE": (255, 50, 60),
            "COLOR_FRAME": (35, 65, 115),  # Deep Rally Blue
            "COLOR_REDLINE": (255, 30, 85, 110),
        },
    },
    "gt3_racing": {
        "name": "GT3 Competition",
        "description": "Modern endurance cockpit: Matte asphalt slate, high-contrast vibrant orange, and turquoise telemetry lines.",
        "colors": {
            "COLOR_BG": (20, 22, 25),
            "COLOR_TEXT_MAIN": (250, 250, 250),
            "COLOR_TEXT_DIM": (160, 165, 175),
            "COLOR_RPM_NORMAL": (255, 120, 0),  # Vibrant GT Orange
            "COLOR_RPM_WARNING": (255, 20, 40),
            "COLOR_THROTTLE": (0, 230, 180),  # Petrol / Teal
            "COLOR_BRAKE": (255, 45, 55),
            "COLOR_FRAME": (70, 75, 85),
            "COLOR_REDLINE": (255, 120, 0, 90),
        },
    },
    "night_neon": {
        "name": "Night Stage Neon (Cyberpunk)",
        "description": "OLED deep black night stage theme with electric cyan and vivid magenta shift warnings.",
        "colors": {
            "COLOR_BG": (10, 10, 14),
            "COLOR_TEXT_MAIN": (255, 255, 255),
            "COLOR_TEXT_DIM": (170, 170, 195),
            "COLOR_RPM_NORMAL": (0, 245, 255),  # Electric Cyan
            "COLOR_RPM_WARNING": (255, 0, 128),  # Neon Magenta
            "COLOR_THROTTLE": (0, 255, 136),
            "COLOR_BRAKE": (255, 20, 80),
            "COLOR_FRAME": (90, 40, 130),  # Neon Violet
            "COLOR_REDLINE": (255, 0, 128, 120),
        },
    },
    "retro_amber": {
        "name": "Retro 90s Amber",
        "description": "Classic 1990s analogue instrument cluster with soothing monochrome warm amber illumination.",
        "colors": {
            "COLOR_BG": (18, 16, 14),
            "COLOR_TEXT_MAIN": (255, 185, 60),  # Warm Amber
            "COLOR_TEXT_DIM": (180, 125, 40),
            "COLOR_RPM_NORMAL": (255, 165, 0),  # Classic Amber Orange
            "COLOR_RPM_WARNING": (255, 50, 20),  # Intense Red-Orange
            "COLOR_THROTTLE": (200, 220, 80),
            "COLOR_BRAKE": (255, 60, 40),
            "COLOR_FRAME": (85, 65, 45),
            "COLOR_REDLINE": (255, 50, 20, 100),
        },
    },
}
