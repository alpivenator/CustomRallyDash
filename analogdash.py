# analogdash.py
# DiRT Rally 2.0 — Analog Telemetry Dashboard
import math
import sys

import pygame

import config
import led_controller
import settings
from udp_listener import UDPListener

try:
    import overlay_win
except ImportError:
    overlay_win = None

# Base dimensions (design resolution)
_BASE_W, _BASE_H = settings.ANALOG_WIDTH, settings.ANALOG_HEIGHT

# Fixed gauge scale (0 – 9000 RPM) independent of car
GAUGE_MAX_RPM = 9000

# Compute scale factor from settings
_scale = settings.TARGET_SCALE if settings.TARGET_SCALE else 1.0

# Effective window size
WIDTH = int(_BASE_W * _scale)
HEIGHT = int(_BASE_H * _scale)


def _s(value):
    """Scale a numeric value by the current scale factor."""
    return int(value * _scale)


def run() -> None:
    """Initialise pygame, start the telemetry loop and render the analog dashboard."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("ANALOG RALLY DASHBOARD")

    # Apply overlay settings on Windows
    if sys.platform == "win32" and config.ENABLE_OVERLAY and overlay_win:
        overlay_win.apply_overlay(
            screen,
            chroma_key=config.OVERLAY_CHROMA_KEY,
            mode=config.OVERLAY_MODE,
            alpha=config.OVERLAY_ALPHA,
        )
        overlay_win.position_window(
            screen, settings.OVERLAY_POSITION, settings.OVERLAY_MARGIN
        )

    # Colour Palette (RGB)
    BG_COLOR = settings.COLOR_BG
    TEXT_MAIN = settings.COLOR_TEXT_MAIN
    TEXT_DIM = settings.COLOR_TEXT_DIM
    RPM_NORMAL = settings.COLOR_RPM_NORMAL
    RPM_WARNING = settings.COLOR_RPM_WARNING
    THR_COLOR = settings.COLOR_THROTTLE
    BRK_COLOR = settings.COLOR_BRAKE
    FRAME_COLOR = settings.COLOR_FRAME
    REDLINE_COLOR = settings.COLOR_REDLINE  # Semi-transparent red

    # Fonts
    font_huge = pygame.font.SysFont("arial", _s(settings.FONT_HUGE_SIZE), bold=True)
    font_large = pygame.font.SysFont("arial", _s(settings.FONT_LARGE_SIZE), bold=True)
    font_small = pygame.font.SysFont("arial", _s(settings.FONT_SMALL_SIZE))
    font_tiny = pygame.font.SysFont("arial", _s(settings.FONT_TINY_SIZE))

    # UDP listener and smoothing state
    listener = UDPListener(config.LISTEN_IP, config.LISTEN_PORT)
    smooth_angle_deg = 135  # Starting needle angle (degrees)
    SMOOTHING_FACTOR = 0.2  # Lower = smoother, higher = more responsive

    clock = pygame.time.Clock()

    # ------------------------------------------------------------------
    # Helper: draw major (nearly every 1/9) and minor (nearly every 1/18) tick marks
    # ------------------------------------------------------------------
    def draw_gauge_markings(
        surface,
        center_x,
        center_y,
        radius,
        start_angle,
        sweep_angle,
    ):
        # Major ticks
        for i in range(10):
            angle_deg = start_angle + (i * 1 / 9 * sweep_angle)
            angle_rad = math.radians(angle_deg)

            inner_x = center_x + (radius - _s(25)) * math.cos(angle_rad)
            inner_y = center_y + (radius - _s(25)) * math.sin(angle_rad)
            outer_x = center_x + (radius - _s(10)) * math.cos(angle_rad)
            outer_y = center_y + (radius - _s(10)) * math.sin(angle_rad)

            pygame.draw.line(
                surface, TEXT_MAIN, (inner_x, inner_y), (outer_x, outer_y), 3
            )

            rpm_value = i * GAUGE_MAX_RPM // 9
            if rpm_value <= GAUGE_MAX_RPM:
                label = font_tiny.render(f"{rpm_value//1000}k", True, TEXT_MAIN)
                label_x = center_x + (radius - _s(40)) * math.cos(angle_rad)
                label_y = center_y + (radius - _s(40)) * math.sin(angle_rad)
                label_rect = label.get_rect(center=(label_x, label_y))
                surface.blit(label, label_rect)

        # Minor ticks
        for i in range(1, 18, 2):
            if i % 2 == 1:
                angle_deg = start_angle + (i * 1 / 18 * sweep_angle)
                angle_rad = math.radians(angle_deg)

                inner_x = center_x + (radius - _s(20)) * math.cos(angle_rad)
                inner_y = center_y + (radius - _s(20)) * math.sin(angle_rad)
                outer_x = center_x + (radius - _s(10)) * math.cos(angle_rad)
                outer_y = center_y + (radius - _s(10)) * math.sin(angle_rad)

                pygame.draw.line(
                    surface, TEXT_MAIN, (inner_x, inner_y), (outer_x, outer_y), 1
                )

    # ------------------------------------------------------------------
    # Helper: draw the red danger zone from car's max_rpm to GAUGE_MAX_RPM
    # ------------------------------------------------------------------
    def draw_redline_zone(
        surface,
        center_x,
        center_y,
        radius,
        start_angle,
        sweep_angle,
        redline_start_ratio,
    ):
        redline_end_ratio = 1.00

        redline_start_angle = start_angle + (redline_start_ratio * sweep_angle)
        redline_end_angle = start_angle + (redline_end_ratio * sweep_angle)

        # Use a separate surface with SRCALPHA for transparency
        redline_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)

        # pygame.draw.arc uses counterclockwise angles; convert:
        #   pygame_angle = -needle_angle
        pygame_start = math.radians(-redline_end_angle)
        pygame_end = math.radians(-redline_start_angle)
        pygame.draw.arc(
            redline_surface,
            REDLINE_COLOR,
            (0, 0, radius * 2, radius * 2),
            pygame_start,
            pygame_end,
            radius - _s(10),
        )

        surface.blit(redline_surface, (center_x - radius, center_y - radius))

    # ------------------------------------------------------------------
    # Main telemetry loop
    # ------------------------------------------------------------------
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

            wheel_speed_kmh = data.wheel_speed_kmh
            rpm = data.rpm
            max_rpm = data.max_rpm
            gear_str = data.gear_str
            throttle = data.throttle
            brake = data.brake

            # --- GRAPHICS ---
            screen.fill(BG_COLOR)

            # Gauge geometry
            center_x, center_y = _s(300), _s(170)
            radius = _s(140)

            # Ratios relative to the fixed 0-9000 scale
            rpm_ratio = max(0.0, min(1.0, rpm / GAUGE_MAX_RPM))
            # Redline starts at the car's actual max_rpm
            redline_start_ratio = min(1.0, max_rpm / GAUGE_MAX_RPM)

            # Update physical shift-light LEDs
            led_controller.update_leds(rpm_ratio)

            start_angle = 135
            sweep_angle = 270

            # Smooth needle movement via linear interpolation
            target_angle_deg = start_angle + (rpm_ratio * sweep_angle)
            smooth_angle_deg += (target_angle_deg - smooth_angle_deg) * SMOOTHING_FACTOR

            # Draw redline zone (car's max_rpm → 9000)
            draw_redline_zone(
                screen,
                center_x,
                center_y,
                radius,
                start_angle,
                sweep_angle,
                redline_start_ratio,
            )

            # Draw tick marks and RPM labels
            draw_gauge_markings(
                screen, center_x, center_y, radius, start_angle, sweep_angle
            )

            # Outer ring
            pygame.draw.circle(screen, FRAME_COLOR, (center_x, center_y), radius, 4)

            # Needle trigonometry
            current_angle_rad = math.radians(smooth_angle_deg)
            needle_end_x = center_x + (radius - _s(15)) * math.cos(current_angle_rad)
            needle_end_y = center_y + (radius - _s(15)) * math.sin(current_angle_rad)

            # Needle colour: red when in car's redline zone
            needle_color = RPM_WARNING if rpm_ratio >= redline_start_ratio else RPM_NORMAL

            pygame.draw.line(
                screen,
                needle_color,
                (center_x, center_y),
                (needle_end_x, needle_end_y),
                6,
            )

            # Pivot point
            pygame.draw.circle(screen, needle_color, (center_x, center_y), _s(8))
            pygame.draw.circle(screen, BG_COLOR, (center_x, center_y), _s(4))

            # Gear circle (background + border + text)
            pygame.draw.circle(screen, BG_COLOR, (center_x, center_y), _s(50))
            pygame.draw.circle(screen, needle_color, (center_x, center_y), _s(50), 2)

            text_gear = font_huge.render(gear_str, True, TEXT_MAIN)
            screen.blit(
                text_gear,
                (
                    center_x - text_gear.get_width() // 2,
                    center_y - text_gear.get_height() // 2.1,
                ),
            )

            # --- LEFT: BRAKE BAR (vertical, left of gauge) ---
            bar_w, max_h = _s(35), _s(130)
            brk_x = center_x - radius - _s(70)
            brk_y = center_y - max_h // 2

            brk_h = int(max_h * brake)

            pygame.draw.rect(
                screen, BRK_COLOR, (brk_x, brk_y + (max_h - brk_h), bar_w, brk_h)
            )
            pygame.draw.rect(screen, FRAME_COLOR, (brk_x, brk_y, bar_w, max_h), 2)
            screen.blit(
                font_small.render("BRK", True, TEXT_DIM),
                (
                    brk_x + bar_w // 2 - font_small.size("BRK")[0] // 2,
                    brk_y + max_h + _s(8),
                ),
            )

            # --- RIGHT: THROTTLE BAR (vertical, right of gauge) ---
            thr_x = center_x + radius + _s(35)
            thr_y = center_y - max_h // 2

            thr_h = int(max_h * throttle)

            pygame.draw.rect(
                screen, THR_COLOR, (thr_x, thr_y + (max_h - thr_h), bar_w, thr_h)
            )
            pygame.draw.rect(screen, FRAME_COLOR, (thr_x, thr_y, bar_w, max_h), 2)
            screen.blit(
                font_small.render("THR", True, TEXT_DIM),
                (
                    thr_x + bar_w // 2 - font_small.size("THR")[0] // 2,
                    thr_y + max_h + _s(8),
                ),
            )

            # --- BOTTOM CENTRE: DIGITAL SPEED (in needle-free arc) ---
            text_speed_lbl = font_small.render("KM/H", True, TEXT_DIM)
            text_speed = font_large.render(f"{wheel_speed_kmh:03d}", True, TEXT_MAIN)
            screen.blit(
                text_speed_lbl,
                (center_x - text_speed_lbl.get_width() // 2, center_y + radius - _s(75)),
            )
            screen.blit(
                text_speed,
                (center_x - text_speed.get_width() // 2, center_y + radius - _s(50)),
            )

            pygame.display.flip()
            clock.tick(60)

    finally:
        led_controller.cleanup()
        listener.close()


if __name__ == "__main__":
    run()
