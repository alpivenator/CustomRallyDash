# tests/test_themes_and_mock.py
"""Unit tests for mock telemetry packet generator and theme management."""

from __future__ import annotations

import struct
from pathlib import Path

from dashboards.themes import THEMES
from tools.mock_telemetry import generate_packet
from tools.theme_selector import apply_theme_to_settings


def test_generate_packet_size_and_fields():
    """Verify that mock generator produces valid 264-byte Extradata=3 packets."""
    packet, speed, rpm, thr, gear = generate_packet(elapsed_time=5.0)

    assert isinstance(packet, bytes)
    assert len(packet) == 264

    # Unpack 66 floats
    fields = struct.unpack("66f", packet)
    assert len(fields) == 66

    # Verify key indices
    car_speed_ms = fields[7]
    assert abs(car_speed_ms - (speed / 3.6)) < 1e-3

    throttle = fields[29]
    assert throttle == thr

    gear_val = int(fields[33])
    assert str(gear_val) == gear

    rpm_unscaled = fields[37]
    assert abs((rpm_unscaled * 10.0) - rpm) < 1.0


def test_theme_definitions():
    """Ensure all predefined themes contain required colour keys."""
    required_colors = {
        "COLOR_BG",
        "COLOR_TEXT_MAIN",
        "COLOR_TEXT_DIM",
        "COLOR_RPM_NORMAL",
        "COLOR_RPM_WARNING",
        "COLOR_THROTTLE",
        "COLOR_BRAKE",
        "COLOR_FRAME",
        "COLOR_REDLINE",
    }

    assert "modern_dark" in THEMES
    assert "subaru_classic" in THEMES
    assert "gt3_racing" in THEMES
    assert "night_neon" in THEMES
    assert "retro_amber" in THEMES

    for key, theme in THEMES.items():
        assert "name" in theme
        assert "description" in theme
        assert "colors" in theme
        assert required_colors.issubset(set(theme["colors"].keys()))


def test_apply_theme_to_settings_temp(tmp_path: Path):
    """Test applying a theme safely updates a settings.py file."""
    mock_settings = tmp_path / "settings.py"
    mock_settings.write_text(
        "COLOR_BG = (0, 0, 0)\nCOLOR_RPM_NORMAL = (10, 20, 30)\n",
        encoding="utf-8",
    )

    success = apply_theme_to_settings(
        "subaru_classic",
        settings_path=mock_settings,
        output_func=lambda msg: None,
        lang="en",
    )

    assert success is True
    content = mock_settings.read_text(encoding="utf-8")
    assert "COLOR_BG = (12, 18, 32)" in content
    assert "COLOR_RPM_NORMAL = (255, 204, 0)" in content


def test_rpm_warning_threshold_setting():
    """Verify that settings.py defines a valid RPM_WARNING_THRESHOLD float."""
    import settings

    assert hasattr(settings, "RPM_WARNING_THRESHOLD")
    assert isinstance(settings.RPM_WARNING_THRESHOLD, (int, float))
    assert 0.0 < settings.RPM_WARNING_THRESHOLD <= 1.0


def test_overlay_settings_structure():
    """Verify that overlay visual settings are properly located in settings.py."""
    import config
    import settings

    # config.py must contain ENABLE_OVERLAY
    assert hasattr(config, "ENABLE_OVERLAY")
    assert isinstance(config.ENABLE_OVERLAY, bool)

    # settings.py must contain overlay layout and transparency options
    assert hasattr(settings, "OVERLAY_MODE")
    assert settings.OVERLAY_MODE in ("chroma", "alpha")
    assert hasattr(settings, "OVERLAY_POSITION")
    assert settings.OVERLAY_POSITION in ("bottom-left", "bottom-center", "bottom-right")
    assert hasattr(settings, "OVERLAY_MARGIN")
    assert isinstance(settings.OVERLAY_MARGIN, int)
    assert hasattr(settings, "OVERLAY_CHROMA_KEY")
    assert settings.OVERLAY_CHROMA_KEY == settings.COLOR_BG


def test_text_outline_rendering():
    """Verify that draw_text_outlined executes and returns a valid rect."""
    import pygame

    from dashboards.digital_dash import draw_text_outlined

    pygame.init()
    surface = pygame.Surface((200, 100))
    font = pygame.font.SysFont("arial", 20)
    rect = draw_text_outlined(
        surface, font, "TEST", (10, 10), (255, 255, 255), (0, 0, 0), outline_px=1
    )
    assert isinstance(rect, pygame.Rect)
    assert rect.width > 0
    assert rect.height > 0

