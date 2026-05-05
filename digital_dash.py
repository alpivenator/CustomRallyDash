# digital_dash.py
import socket
import struct
import pygame
import sys
import config
import led_controller

# Import overlay_win if available (may not exist on Linux or if file is missing)
try:
    import overlay_win
except ImportError:
    overlay_win = None

# --- 1. UDP NETWORK SETUP ---
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((config.LISTEN_IP, config.LISTEN_PORT))
sock.settimeout(0.01)

# --- 2. PYGAME UI SETUP ---
pygame.init()
WIDTH, HEIGHT = 600, 200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MODERN RALLY DASHBOARD")

# Apply overlay on Windows if enabled in config
if sys.platform == "win32" and config.ENABLE_OVERLAY and overlay_win:
    overlay_win.apply_overlay(screen, config.OVERLAY_CHROMA_KEY)
    if config.OVERLAY_BOTTOM_CENTER:
        overlay_win.position_window_bottom_center(screen)
else:
    pass

# Color Palette (RGB)
BG_COLOR = (25, 25, 30)
TEXT_MAIN = (240, 240, 240)
TEXT_DIM = (120, 120, 130)
RPM_NORMAL = (0, 150, 255)
RPM_WARNING = (255, 40, 40)
THR_COLOR = (40, 220, 100)
BRK_COLOR = (255, 60, 60)
FRAME_COLOR = (80, 80, 90)

# Fonts - optimized
font_huge = pygame.font.SysFont("arial", 64, bold=True)  # Large for gear
font_large = pygame.font.SysFont("arial", 48, bold=True)  # Large for speed
font_medium = pygame.font.SysFont("arial", 20, bold=True)  # RPM value
font_small = pygame.font.SysFont("arial", 18)  # For labels
font_tiny = pygame.font.SysFont("arial", 14)  # Small labels

# Telemetry Variables
wheel_speed_kmh = 0
car_speed_kmh = 0
rpm = 0
max_rpm = 8000
gear_str = "N"
throttle = 0.0
brake = 0.0

clock = pygame.time.Clock()

# --- 3. MAIN LOOP ---
try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                led_controller.cleanup()
                sys.exit()

        # Buffer Draining
        last_packet = None
        try:
            while True:
                data, addr = sock.recvfrom(1024)
                if len(data) == 264:
                    last_packet = data
        except socket.timeout:
            pass

        # Data Parsing
        if last_packet:
            unpacked = struct.unpack("66f", last_packet)

            car_speed_kmh = int(unpacked[7] * 3.6)

            speed_ms = (unpacked[25] + unpacked[26] + unpacked[27] + unpacked[28]) / 4
            wheel_speed_kmh = int(speed_ms * 3.6)

            rpm = int(unpacked[37] * 10)
            read_max_rpm = int(unpacked[63] * 10)
            if read_max_rpm > 0:
                max_rpm = read_max_rpm

            gear = int(unpacked[33])
            if gear == 0:
                gear_str = "N"
            elif gear == -1:
                gear_str = "R"
            else:
                gear_str = str(gear)

            throttle = max(0.0, min(1.0, unpacked[29]))
            brake = max(0.0, min(1.0, unpacked[31]))

        # --- GRAPHICS DRAWING ---
        screen.fill(BG_COLOR)

        # 1. TOP: RPM BAR
        bar_x, bar_y = 30, 20
        bar_max_w, bar_h = 540, 25

        rpm_ratio = max(0.0, min(1.0, rpm / max_rpm))
        bar_current_w = int(bar_max_w * rpm_ratio)

        # Hardware LED update
        led_controller.update_leds(rpm_ratio)

        if rpm_ratio >= 0.90:
            bar_color = RPM_WARNING
        else:
            bar_color = RPM_NORMAL

        pygame.draw.rect(screen, bar_color, (bar_x, bar_y, bar_current_w, bar_h))
        pygame.draw.rect(screen, FRAME_COLOR, (bar_x, bar_y, bar_max_w, bar_h), 2)

        # RPM value - bottom right of the bar
        text_rpm = font_medium.render(f"{rpm} RPM", True, TEXT_MAIN)
        screen.blit(
            text_rpm, (bar_x + bar_max_w - text_rpm.get_width(), bar_y + bar_h + 5)
        )

        # 2. LEFT: GEAR
        text_gear_lbl = font_small.render("GEAR", True, TEXT_DIM)
        text_gear = font_huge.render(gear_str, True, TEXT_MAIN)
        screen.blit(text_gear_lbl, (30, 60))
        screen.blit(text_gear, (30, 85))

        # 3. SPEED
        text_speed_lbl = font_small.render("SPEED", True, TEXT_DIM)
        text_speed = font_large.render(f"{wheel_speed_kmh:03d}", True, TEXT_MAIN)

        speed_x = 200
        speed_lbl_x = 200

        screen.blit(text_speed_lbl, (speed_lbl_x, 60))
        screen.blit(text_speed, (speed_x, 85))

        # 4. RIGHT: HORIZONTAL PEDAL BARS
        # Throttle bar (top)
        thr_bar_x, thr_bar_y = 350, 90
        thr_bar_w, thr_bar_h = 200, 20

        thr_current_w = int(thr_bar_w * throttle)

        pygame.draw.rect(
            screen, THR_COLOR, (thr_bar_x, thr_bar_y, thr_current_w, thr_bar_h)
        )
        pygame.draw.rect(
            screen, FRAME_COLOR, (thr_bar_x, thr_bar_y, thr_bar_w, thr_bar_h), 2
        )

        # Throttle label
        text_thr = font_tiny.render("THR", True, TEXT_DIM)
        screen.blit(text_thr, (thr_bar_x + thr_bar_w + 5, thr_bar_y + 3))

        # Brake bar (bottom)
        brk_bar_x, brk_bar_y = 350, 120
        brk_bar_w, brk_bar_h = 200, 20

        brk_current_w = int(brk_bar_w * brake)

        pygame.draw.rect(
            screen, BRK_COLOR, (brk_bar_x, brk_bar_y, brk_current_w, brk_bar_h)
        )
        pygame.draw.rect(
            screen, FRAME_COLOR, (brk_bar_x, brk_bar_y, brk_bar_w, brk_bar_h), 2
        )

        # Brake label
        text_brk = font_tiny.render("BRK", True, TEXT_DIM)
        screen.blit(text_brk, (brk_bar_x + brk_bar_w + 5, brk_bar_y + 3))

        pygame.display.flip()
        clock.tick(60)

finally:
    led_controller.cleanup()
