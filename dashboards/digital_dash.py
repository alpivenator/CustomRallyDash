# dashboards/digital_dash.py
# DiRT Rally 2.0 — Digital Telemetry Dashboard
import sys

import pygame

import config
import settings
from core import led_controller
from core.udp_listener import UDPListener

# Import overlay_win if available (Windows only)
try:
    from core import overlay_win
except ImportError:
    overlay_win = None

# Base dimensions (design resolution)
_BASE_W, _BASE_H = settings.DIGITAL_WIDTH, settings.DIGITAL_HEIGHT

# Compute scale factor from settings
_scale = settings.TARGET_SCALE if settings.TARGET_SCALE else 1.0

# Effective window size
WIDTH = int(_BASE_W * _scale)
HEIGHT = int(_BASE_H * _scale)


def _s(value):
    """Scale a numeric value by the current scale factor."""
    return int(value * _scale)


def draw_text_outlined(
    surface: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    pos: tuple[int, int],
    color: tuple[int, int, int],
    outline_color: tuple[int, int, int] = (0, 0, 0),
    outline_px: int = 1,
) -> pygame.Rect:
    """Render text with a dark outer stroke for high readability on transparent HUD overlays."""
    x, y = pos
    px = max(1, _s(outline_px))
    outline_surf = font.render(text, True, outline_color)
    for dx in (-px, 0, px):
        for dy in (-px, 0, px):
            if dx != 0 or dy != 0:
                surface.blit(outline_surf, (x + dx, y + dy))
    text_surf = font.render(text, True, color)
    return surface.blit(text_surf, (x, y))


def run() -> None:
    """Initialise pygame, start the telemetry loop and render the digital dashboard."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("MODERN RALLY DASHBOARD")

    # Apply overlay settings on Windows
    if sys.platform == "win32" and config.ENABLE_OVERLAY and overlay_win:
        overlay_win.apply_overlay(
            screen,
            chroma_key=settings.OVERLAY_CHROMA_KEY,
            mode=settings.OVERLAY_MODE,
            alpha=settings.OVERLAY_ALPHA,
        )
        overlay_win.position_window(
            screen, settings.OVERLAY_POSITION, settings.OVERLAY_MARGIN
        )

    # Colour Palette (RGB)
    BG_COLOR = settings.COLOR_BG
    TEXT_MAIN = settings.COLOR_TEXT_MAIN
    TEXT_DIM = settings.COLOR_TEXT_DIM
    TEXT_OUTLINE = getattr(settings, "COLOR_TEXT_OUTLINE", (0, 0, 0))
    RPM_NORMAL = settings.COLOR_RPM_NORMAL
    RPM_WARNING = settings.COLOR_RPM_WARNING
    THR_COLOR = settings.COLOR_THROTTLE
    BRK_COLOR = settings.COLOR_BRAKE
    FRAME_COLOR = settings.COLOR_FRAME

    # Fonts — optimised for small overlay window
    font_huge = pygame.font.SysFont("arial", _s(settings.FONT_HUGE_SIZE), bold=True)
    font_large = pygame.font.SysFont("arial", _s(settings.FONT_LARGE_SIZE), bold=True)
    font_medium = pygame.font.SysFont("arial", _s(settings.FONT_MEDIUM_SIZE), bold=True)
    font_small = pygame.font.SysFont("arial", _s(settings.FONT_SMALL_SIZE), bold=True)
    font_tiny = pygame.font.SysFont("arial", _s(settings.FONT_TINY_SIZE), bold=True)

    # Initialise UDP listener and clock
    listener = UDPListener(config.LISTEN_IP, config.LISTEN_PORT)
    clock = pygame.time.Clock()

    try:
        while True:
            # Handle window close events
            try:
                events = pygame.event.get()
            except SystemError:
                events = []
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    led_controller.cleanup()
                    sys.exit()

            # Fetch latest telemetry from UDP
            data = listener.receive()

            rpm = data.rpm
            max_rpm = data.max_rpm
            gear_str = data.gear_str
            wheel_speed_kmh = data.wheel_speed_kmh
            throttle = data.throttle
            brake = data.brake

            # --- GRAPHICS ---
            screen.fill(BG_COLOR)

            # 1. TOP: RPM BAR
            bar_x, bar_y = _s(30), _s(20)
            bar_max_w, bar_h = _s(540), _s(25)

            rpm_ratio = max(0.0, min(1.0, rpm / max_rpm))
            bar_current_w = int(bar_max_w * rpm_ratio)

            # Update physical shift-light LEDs
            led_controller.update_leds(rpm_ratio)

            # Colour changes to red when reaching warning threshold
            bar_color = (
                RPM_WARNING if rpm_ratio >= settings.RPM_WARNING_THRESHOLD else RPM_NORMAL
            )

            pygame.draw.rect(screen, bar_color, (bar_x, bar_y, bar_current_w, bar_h))
            pygame.draw.rect(screen, FRAME_COLOR, (bar_x, bar_y, bar_max_w, bar_h), 2)

            # RPM label — bottom-right of the bar
            rpm_text_str = f"{rpm} RPM"
            rpm_text_w = font_medium.size(rpm_text_str)[0]
            draw_text_outlined(
                screen,
                font_medium,
                rpm_text_str,
                (bar_x + bar_max_w - rpm_text_w, bar_y + bar_h + _s(5)),
                TEXT_MAIN,
                TEXT_OUTLINE,
                outline_px=1,
            )

            # 2. LEFT: SPEED
            speed_str = f"{wheel_speed_kmh:03d}"
            draw_text_outlined(
                screen,
                font_small,
                "SPEED",
                (_s(30), _s(60)),
                TEXT_DIM,
                TEXT_OUTLINE,
                outline_px=1,
            )
            draw_text_outlined(
                screen,
                font_large,
                speed_str,
                (_s(30), _s(85)),
                TEXT_MAIN,
                TEXT_OUTLINE,
                outline_px=1,
            )

            # 3. CENTRE: GEAR
            gear_cx = _s(260)
            gear_lbl_w = font_small.size("GEAR")[0]
            draw_text_outlined(
                screen,
                font_small,
                "GEAR",
                (gear_cx - gear_lbl_w // 2, _s(60)),
                TEXT_DIM,
                TEXT_OUTLINE,
                outline_px=1,
            )

            gear_w = font_huge.size(gear_str)[0]
            draw_text_outlined(
                screen,
                font_huge,
                gear_str,
                (gear_cx - gear_w // 2, _s(80)),
                TEXT_MAIN,
                TEXT_OUTLINE,
                outline_px=2,
            )

            # 4. RIGHT: HORIZONTAL PEDAL BARS
            # Throttle (top bar)
            thr_bar_x, thr_bar_y = _s(350), _s(90)
            thr_bar_w, thr_bar_h = _s(200), _s(20)

            thr_current_w = int(thr_bar_w * throttle)

            pygame.draw.rect(
                screen, THR_COLOR, (thr_bar_x, thr_bar_y, thr_current_w, thr_bar_h)
            )
            pygame.draw.rect(
                screen, FRAME_COLOR, (thr_bar_x, thr_bar_y, thr_bar_w, thr_bar_h), 2
            )

            draw_text_outlined(
                screen,
                font_tiny,
                "THR",
                (thr_bar_x + thr_bar_w + _s(5), thr_bar_y + _s(3)),
                TEXT_DIM,
                TEXT_OUTLINE,
                outline_px=1,
            )

            # Brake (bottom bar)
            brk_bar_x, brk_bar_y = _s(350), _s(120)
            brk_bar_w, brk_bar_h = _s(200), _s(20)

            brk_current_w = int(brk_bar_w * brake)

            pygame.draw.rect(
                screen, BRK_COLOR, (brk_bar_x, brk_bar_y, brk_current_w, brk_bar_h)
            )
            pygame.draw.rect(
                screen, FRAME_COLOR, (brk_bar_x, brk_bar_y, brk_bar_w, brk_bar_h), 2
            )

            draw_text_outlined(
                screen,
                font_tiny,
                "BRK",
                (brk_bar_x + brk_bar_w + _s(5), brk_bar_y + _s(3)),
                TEXT_DIM,
                TEXT_OUTLINE,
                outline_px=1,
            )

            pygame.display.flip()
            clock.tick(60)


    finally:
        led_controller.cleanup()
        listener.close()


if __name__ == "__main__":
    run()
