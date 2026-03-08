# analog_dash.py
import socket
import struct
import pygame
import sys
import math
import config
import led_controller

# --- 1. UDP NETWORK SETUP ---
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((config.LISTEN_IP, config.LISTEN_PORT))
sock.settimeout(0.01)

# --- 2. PYGAME UI SETUP ---
pygame.init()
WIDTH, HEIGHT = 800, 400 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RALLY TELEMETRY - ANALOG EDITION")

# Color Palette (RGB)
BG_COLOR = (25, 25, 30)
TEXT_MAIN = (240, 240, 240)
TEXT_DIM = (120, 120, 130)
RPM_NORMAL = (0, 150, 255)
RPM_WARNING = (255, 40, 40)
THR_COLOR = (40, 220, 100)
BRK_COLOR = (255, 60, 60)
FRAME_COLOR = (80, 80, 90)

# Fonts
font_huge = pygame.font.SysFont("arial", 96, bold=True)
font_large = pygame.font.SysFont("arial", 48, bold=True)
font_small = pygame.font.SysFont("arial", 20)

# Telemetry Variables
wheel_speed_kmh = 0
rpm = 0
max_rpm = 8000 # Fallback value, gets overwritten dynamically by UDP
gear_str = "N"
throttle = 0.0
brake = 0.0

clock = pygame.time.Clock()

# --- 3. MAIN LOOP ---
try:
    while True:
        # Event Handling
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
            unpacked = struct.unpack('66f', last_packet)
            
            speed_ms = (unpacked[25] + unpacked[26] + unpacked[27] + unpacked[28]) / 4
            wheel_speed_kmh = int(speed_ms * 3.6)
            
            rpm = int(unpacked[37] * 10)
            read_max_rpm = int(unpacked[63] * 10)
            
            # Dynamically update MAX_RPM if the game sends a valid number
            if read_max_rpm > 0: 
                max_rpm = read_max_rpm
            
            gear = int(unpacked[33])
            if gear == 0: gear_str = "N"
            elif gear == -1: gear_str = "R"
            else: gear_str = str(gear)
                
            throttle = max(0.0, min(1.0, unpacked[29]))
            brake = max(0.0, min(1.0, unpacked[31]))

        # --- 4. GRAPHICS DRAWING ---
        screen.fill(BG_COLOR)

        # Center of the gauge on the left side
        center_x, center_y = 250, 220
        radius = 160
        
        # Calculate ratio using the dynamic max_rpm
        rpm_ratio = max(0.0, min(1.0, rpm / max_rpm))
        
        # Hardware LED update
        led_controller.update_leds(rpm_ratio)

        # Draw outer circle for the gauge
        pygame.draw.circle(screen, FRAME_COLOR, (center_x, center_y), radius, 4)
        
        # Calculate Needle Angle (135 degrees to 405 degrees)
        start_angle = 135
        sweep_angle = 270
        current_angle_deg = start_angle + (rpm_ratio * sweep_angle)
        
        # Convert degrees to radians for math functions
        current_angle_rad = math.radians(current_angle_deg)
        
        # Calculate needle endpoint using Trigonometry
        needle_end_x = center_x + (radius - 10) * math.cos(current_angle_rad)
        needle_end_y = center_y + (radius - 10) * math.sin(current_angle_rad)
        
        # Determine needle color
        needle_color = RPM_WARNING if rpm_ratio >= 0.90 else RPM_NORMAL
        
        # Draw the needle line
        pygame.draw.line(screen, needle_color, (center_x, center_y), (needle_end_x, needle_end_y), 6)
        
        # Draw the Gear in the exact center of the gauge
        text_gear = font_huge.render(gear_str, True, TEXT_MAIN)
        gear_rect = text_gear.get_rect(center=(center_x, center_y))
        
        # Draw a small background circle for the gear text to make it readable
        pygame.draw.circle(screen, BG_COLOR, (center_x, center_y), 50)
        pygame.draw.circle(screen, needle_color, (center_x, center_y), 50, 2)
        screen.blit(text_gear, gear_rect)

        # --- RIGHT SIDE: SPEED AND PEDALS ---
        # Speedometer Text
        text_speed_lbl = font_small.render("SPEED (KM/H)", True, TEXT_DIM)
        text_speed = font_large.render(f"{wheel_speed_kmh:03d}", True, TEXT_MAIN)
        screen.blit(text_speed_lbl, (550, 50))
        screen.blit(text_speed, (550, 80))

        # Pedals
        bar_w, max_h = 150, 40 # Inverted w/h variables conceptually, but lets keep the logic straight
        # To avoid confusion: the original code used bar_w=40, max_h=150
        bar_w, max_h = 40, 150
        brk_x, brk_y = 550, 180
        thr_x, thr_y = 620, 180
        
        brk_h = int(max_h * brake)
        thr_h = int(max_h * throttle)

        # Brake Bar
        pygame.draw.rect(screen, BRK_COLOR, (brk_x, brk_y + (max_h - brk_h), bar_w, brk_h))
        pygame.draw.rect(screen, FRAME_COLOR, (brk_x, brk_y, bar_w, max_h), 2)
        screen.blit(font_small.render("BRK", True, TEXT_DIM), (brk_x, brk_y + max_h + 10))

        # Throttle Bar
        pygame.draw.rect(screen, THR_COLOR, (thr_x, thr_y + (max_h - thr_h), bar_w, thr_h))
        pygame.draw.rect(screen, FRAME_COLOR, (thr_x, thr_y, bar_w, max_h), 2)
        screen.blit(font_small.render("THR", True, TEXT_DIM), (thr_x, thr_y + max_h + 10))

        # Update Screen
        pygame.display.flip()
        clock.tick(60)

finally:
    led_controller.cleanup()