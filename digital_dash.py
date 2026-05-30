# digital_dash.py
# DiRT Rally 2.0 — Digital Telemetry Dashboard
import sys

import pygame

import config
import led_controller
from udp_listener import UDPListener

# Import overlay_win if available (Windows only)
try:
    import overlay_win
except ImportError:
    overlay_win = None

WIDTH, HEIGHT = 600, 200


def run() -> None:
    """Initialise pygame, start the telemetry loop and render the digital dashboard."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("MODERN RALLY DASHBOARD")

    # Apply overlay settings on Windows
    if sys.platform == "win32" and config.ENABLE_OVERLAY and overlay_win:
        overlay_win.apply_overlay(
            screen,
            chroma_key=config.OVERLAY_CHROMA_KEY,
            mode=config.OVERLAY_MODE,
            alpha=config.OVERLAY_ALPHA,
        )
        if config.OVERLAY_BOTTOM_CENTER:
            overlay_win.position_window_bottom_center(screen)

    # Colour Palette (RGB)
    BG_COLOR = (25, 25, 30)
    TEXT_MAIN = (240, 240, 240)
    TEXT_DIM = (120, 120, 130)
    RPM_NORMAL = (0, 150, 255)
    RPM_WARNING = (255, 40, 40)
    THR_COLOR = (40, 220, 100)
    BRK_COLOR = (255, 60, 60)
    FRAME_COLOR = (80, 80, 90)

    # Fonts — optimised for small overlay window
    font_huge = pygame.font.SysFont("arial", 80, bold=True)  # Gear number
    font_large = pygame.font.SysFont("arial", 48, bold=True)  # Speed value
    font_medium = pygame.font.SysFont("arial", 20, bold=True)  # RPM value
    font_small = pygame.font.SysFont("arial", 18)  # Labels
    font_tiny = pygame.font.SysFont("arial", 14)  # Small labels

    # Initialise UDP listener and clock
    listener = UDPListener(config.LISTEN_IP, config.LISTEN_PORT)
    clock = pygame.time.Clock()

    try:
        while True:
            # Handle window close events
            for event in pygame.event.get():
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
            bar_x, bar_y = 30, 20
            bar_max_w, bar_h = 540, 25

            rpm_ratio = max(0.0, min(1.0, rpm / max_rpm))
            bar_current_w = int(bar_max_w * rpm_ratio)

            # Update physical shift-light LEDs
            led_controller.update_leds(rpm_ratio)

            # Colour changes to red when above 90% redline
            bar_color = RPM_WARNING if rpm_ratio >= 0.90 else RPM_NORMAL

            pygame.draw.rect(screen, bar_color, (bar_x, bar_y, bar_current_w, bar_h))
            pygame.draw.rect(screen, FRAME_COLOR, (bar_x, bar_y, bar_max_w, bar_h), 2)

            # RPM label — bottom-right of the bar
            text_rpm = font_medium.render(f"{rpm} RPM", True, TEXT_MAIN)
            screen.blit(
                text_rpm, (bar_x + bar_max_w - text_rpm.get_width(), bar_y + bar_h + 5)
            )

            # 2. LEFT: SPEED
            text_speed_lbl = font_small.render("SPEED", True, TEXT_DIM)
            text_speed = font_large.render(f"{wheel_speed_kmh:03d}", True, TEXT_MAIN)
            screen.blit(text_speed_lbl, (30, 60))
            screen.blit(text_speed, (30, 85))

            # 3. CENTRE: GEAR
            text_gear_lbl = font_small.render("GEAR", True, TEXT_DIM)
            text_gear = font_huge.render(gear_str, True, TEXT_MAIN)
            gear_cx = 260
            screen.blit(
                text_gear_lbl,
                (gear_cx - text_gear_lbl.get_width() // 2, 60),
            )
            screen.blit(
                text_gear,
                (gear_cx - text_gear.get_width() // 2, 80),
            )

            # 4. RIGHT: HORIZONTAL PEDAL BARS
            # Throttle (top bar)
            thr_bar_x, thr_bar_y = 350, 90
            thr_bar_w, thr_bar_h = 200, 20

            thr_current_w = int(thr_bar_w * throttle)

            pygame.draw.rect(
                screen, THR_COLOR, (thr_bar_x, thr_bar_y, thr_current_w, thr_bar_h)
            )
            pygame.draw.rect(
                screen, FRAME_COLOR, (thr_bar_x, thr_bar_y, thr_bar_w, thr_bar_h), 2
            )

            text_thr = font_tiny.render("THR", True, TEXT_DIM)
            screen.blit(text_thr, (thr_bar_x + thr_bar_w + 5, thr_bar_y + 3))

            # Brake (bottom bar)
            brk_bar_x, brk_bar_y = 350, 120
            brk_bar_w, brk_bar_h = 200, 20

            brk_current_w = int(brk_bar_w * brake)

            pygame.draw.rect(
                screen, BRK_COLOR, (brk_bar_x, brk_bar_y, brk_current_w, brk_bar_h)
            )
            pygame.draw.rect(
                screen, FRAME_COLOR, (brk_bar_x, brk_bar_y, brk_bar_w, brk_bar_h), 2
            )

            text_brk = font_tiny.render("BRK", True, TEXT_DIM)
            screen.blit(text_brk, (brk_bar_x + brk_bar_w + 5, brk_bar_y + 3))

            pygame.display.flip()
            clock.tick(60)

    finally:
        led_controller.cleanup()
        listener.close()


if __name__ == "__main__":
    run()
