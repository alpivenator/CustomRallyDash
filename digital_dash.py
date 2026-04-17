# digital_dash.py
import socket
import struct
import pygame
import sys
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
pygame.display.set_caption("MODERN RALLY DASHBOARD")

# Color Palette (RGB)
BG_COLOR = (25, 25, 30)
TEXT_MAIN = (240, 240, 240)
TEXT_DIM = (120, 120, 130)
RPM_NORMAL = (0, 150, 255)
RPM_WARNING = (255, 40, 40)
THR_COLOR = (40, 220, 100)
BRK_COLOR = (255, 60, 60)
FRAME_COLOR = (80, 80, 90)
TRACTION_LOSS_COLOR = (255, 200, 0)

# Fonts
font_huge = pygame.font.SysFont("arial", 72, bold=True)
font_large = pygame.font.SysFont("arial", 48, bold=True)
font_medium = pygame.font.SysFont("arial", 32, bold=True)
font_small = pygame.font.SysFont("arial", 20)

# Telemetry Variables
wheel_speed_kmh = 0
car_speed_kmh = 0 
rpm = 0
max_rpm = 8000 # Fallback value, gets overwritten by UDP
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
            unpacked = struct.unpack('66f', last_packet)
            
            car_speed_kmh = int(unpacked[7] * 3.6) 
            
            speed_ms = (unpacked[25] + unpacked[26] + unpacked[27] + unpacked[28]) / 4
            wheel_speed_kmh = int(speed_ms * 3.6) 
            
            rpm = int(unpacked[37] * 10)
            read_max_rpm = int(unpacked[63] * 10)
            if read_max_rpm > 0: 
                max_rpm = read_max_rpm
            
            gear = int(unpacked[33])
            if gear == 0: gear_str = "N" 
            elif gear == -1: gear_str = "R" 
            else: gear_str = str(gear)
                
            throttle = max(0.0, min(1.0, unpacked[29]))
            brake = max(0.0, min(1.0, unpacked[31]))

        # --- GRAPHICS DRAWING ---
        screen.fill(BG_COLOR) 
        
        # Gear
        text_gear_lbl = font_small.render("GEAR", True, TEXT_DIM)
        text_gear = font_huge.render(gear_str, True, TEXT_MAIN)
        screen.blit(text_gear_lbl, (50, 100))
        screen.blit(text_gear, (50, 120))

        # Speed
        text_speed_lbl = font_small.render("SPEED (KM/H)", True, TEXT_DIM)
        text_speed = font_huge.render(f"{wheel_speed_kmh:03d}", True, TEXT_MAIN)
        screen.blit(text_speed_lbl, (250, 100))
        screen.blit(text_speed, (250, 120))

        # RPM Bar
        bar_x, bar_y = 50, 40
        bar_max_w, bar_h = 700, 30
        
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
        
        text_rpm = font_medium.render(f"{rpm} RPM", True, TEXT_MAIN)
        screen.blit(text_rpm, (WIDTH - 200, 80))

        # Traction Loss Warning
        if (wheel_speed_kmh - car_speed_kmh) > 20 and throttle > 0.5:
            pygame.draw.rect(screen, TRACTION_LOSS_COLOR, (450, 120, 120, 35))
            text_slip = font_small.render("SLIP", True, BG_COLOR)
            screen.blit(text_slip, (490, 125))

        # Pedals
        pedal_w, pedal_max_h = 40, 150
        brk_x, brk_y = 600, 150
        thr_x, thr_y = 670, 150
        
        thr_h = int(pedal_max_h * throttle)
        brk_h = int(pedal_max_h * brake)

        pygame.draw.rect(screen, BRK_COLOR, (brk_x, brk_y + (pedal_max_h - brk_h), pedal_w, brk_h))
        pygame.draw.rect(screen, FRAME_COLOR, (brk_x, brk_y, pedal_w, pedal_max_h), 2)
        screen.blit(font_small.render("BRK", True, TEXT_DIM), (brk_x, brk_y + pedal_max_h + 10))

        pygame.draw.rect(screen, THR_COLOR, (thr_x, thr_y + (pedal_max_h - thr_h), pedal_w, thr_h))
        pygame.draw.rect(screen, FRAME_COLOR, (thr_x, thr_y, pedal_w, pedal_max_h), 2)
        screen.blit(font_small.render("THR", True, TEXT_DIM), (thr_x, thr_y + pedal_max_h + 10))

        pygame.display.flip() 
        clock.tick(60)
        
finally:
    led_controller.cleanup()