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
pygame.display.set_caption("ANALOG RALLY DASHBOARD") 

# Color Palette (RGB)
BG_COLOR = (25, 25, 30)
TEXT_MAIN = (240, 240, 240)
TEXT_DIM = (120, 120, 130)
RPM_NORMAL = (0, 150, 255)
RPM_WARNING = (255, 40, 40)
THR_COLOR = (40, 220, 100)
BRK_COLOR = (255, 60, 60)
FRAME_COLOR = (80, 80, 90)
REDLINE_COLOR = (255, 40, 40, 100)  # Semi-transparent red for redline zone

# Fonts
font_huge = pygame.font.SysFont("arial", 96, bold=True)
font_large = pygame.font.SysFont("arial", 48, bold=True)
font_small = pygame.font.SysFont("arial", 20)
font_tiny = pygame.font.SysFont("arial", 16)

# Constant gauge scale (0 - 9000 RPM)
GAUGE_MAX_RPM = 9000

# Telemetry Variables
wheel_speed_kmh = 0
rpm = 0
max_rpm = 8000 # Fallback value, gets overwritten dynamically by UDP
gear_str = "N"
throttle = 0.0
brake = 0.0

# Smoothing variables for needle movement
smooth_angle_deg = 135  # Initial angle
SMOOTHING_FACTOR = 0.2  # Lower = smoother, higher = more responsive

clock = pygame.time.Clock()

# --- Helper Functions ---
def draw_gauge_markings(surface, center_x, center_y, radius, start_angle, sweep_angle):
    # Major ticks (every 10%)
    for i in range(10):  # 0%, 10%, 20%, ..., 100%
        angle_deg = start_angle + (i * 1/9 * sweep_angle)
        angle_rad = math.radians(angle_deg)
        
        inner_x = center_x + (radius - 25) * math.cos(angle_rad)
        inner_y = center_y + (radius - 25) * math.sin(angle_rad)
        outer_x = center_x + (radius - 10) * math.cos(angle_rad)
        outer_y = center_y + (radius - 10) * math.sin(angle_rad)
        
        pygame.draw.line(surface, TEXT_MAIN, (inner_x, inner_y), (outer_x, outer_y), 3)
        
        rpm_value = i * GAUGE_MAX_RPM // 9
        if rpm_value <= GAUGE_MAX_RPM:
            label = font_tiny.render(f"{rpm_value//1000}k", True, TEXT_MAIN)
            label_x = center_x + (radius - 40) * math.cos(angle_rad)
            label_y = center_y + (radius - 40) * math.sin(angle_rad)
            label_rect = label.get_rect(center=(label_x, label_y))
            surface.blit(label, label_rect)
    
    # Minor ticks (every 5%, skip major tick positions)
    for i in range(1, 18, 2):  # 5% to 95%
        if i % 2 == 1:  # odd indices (5%,15%,...,95%) are minor
            angle_deg = start_angle + (i * 1/18 * sweep_angle)
            angle_rad = math.radians(angle_deg)
            
            inner_x = center_x + (radius - 20) * math.cos(angle_rad)
            inner_y = center_y + (radius - 20) * math.sin(angle_rad)
            outer_x = center_x + (radius - 10) * math.cos(angle_rad)
            outer_y = center_y + (radius - 10) * math.sin(angle_rad)
            
            pygame.draw.line(surface, TEXT_MAIN, (inner_x, inner_y), (outer_x, outer_y), 1)

def draw_redline_zone(surface, center_x, center_y, radius, start_angle, sweep_angle, redline_start_ratio):
    """Draw a red warning zone from car's max_rpm to GAUGE_MAX_RPM."""
    redline_end_ratio = 1.00
    
    redline_start_angle = start_angle + (redline_start_ratio * sweep_angle)
    redline_end_angle = start_angle + (redline_end_ratio * sweep_angle)
    
    # Create a surface for the redline zone with transparency
    redline_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    
    # Convert needle angles to pygame arc angles.
    # Needle uses clockwise angles with 0° = right.
    # pygame.draw.arc uses counterclockwise angles with 0° = right.
    # Conversion: pygame_angle = -needle_angle
    # Draw CCW from end_angle to start_angle to match the clockwise sweep.
    pygame_start = math.radians(-redline_end_angle)
    pygame_end   = math.radians(-redline_start_angle)
    pygame.draw.arc(
        redline_surface, 
        REDLINE_COLOR, 
        (0, 0, radius*2, radius*2),
        pygame_start,
        pygame_end,
        radius - 10
    )
    
    # Blit the redline surface onto the main surface
    surface.blit(redline_surface, (center_x - radius, center_y - radius))

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
        
        # Calculate ratio using the constant max_rpm
        rpm_ratio = max(0.0, min(1.0, rpm / GAUGE_MAX_RPM))

        # Redline zone starts at car's actual max_rpm, ends at GAUGE_MAX_RPM
        redline_start_ratio = min(1.0, max_rpm / GAUGE_MAX_RPM)
        
        # Hardware LED update
        led_controller.update_leds(rpm_ratio)

        # Gauge parameters
        start_angle = 135
        sweep_angle = 270
        
        # Calculate target angle
        target_angle_deg = start_angle + (rpm_ratio * sweep_angle)
        
        # Smooth needle movement using linear interpolation
        smooth_angle_deg += (target_angle_deg - smooth_angle_deg) * SMOOTHING_FACTOR
        
        # Draw redline warning zone (from car's max_rpm to GAUGE_MAX_RPM)
        draw_redline_zone(screen, center_x, center_y, radius, start_angle, sweep_angle, redline_start_ratio)
        
        # Draw gauge markings and labels
        draw_gauge_markings(screen, center_x, center_y, radius, start_angle, sweep_angle)
        
        # Draw outer circle for the gauge
        pygame.draw.circle(screen, FRAME_COLOR, (center_x, center_y), radius, 4)
        
        # Convert smoothed angle to radians
        current_angle_rad = math.radians(smooth_angle_deg)
        
        # Calculate needle endpoint using Trigonometry
        needle_end_x = center_x + (radius - 15) * math.cos(current_angle_rad)
        needle_end_y = center_y + (radius - 15) * math.sin(current_angle_rad)
        
        # Determine needle color based on car's redline
        needle_color = RPM_WARNING if rpm_ratio >= redline_start_ratio else RPM_NORMAL
        
        # Draw the needle line
        pygame.draw.line(screen, needle_color, (center_x, center_y), (needle_end_x, needle_end_y), 6)
        
        # Draw needle pivot point (small circle at center)
        pygame.draw.circle(screen, needle_color, (center_x, center_y), 8)
        pygame.draw.circle(screen, BG_COLOR, (center_x, center_y), 4)
        
        # Draw gear background circle FIRST (so it's behind the text)
        pygame.draw.circle(screen, BG_COLOR, (center_x, center_y), 50)
        pygame.draw.circle(screen, needle_color, (center_x, center_y), 50, 2)
        
        # Draw the Gear text - centered properly within the circle
        text_gear = font_huge.render(gear_str, True, TEXT_MAIN)
        screen.blit(text_gear, (center_x - text_gear.get_width() // 2, 
                                center_y - text_gear.get_height() // 2.1))

        # --- RIGHT SIDE: SPEED AND PEDALS ---
        # Speedometer Text
        text_speed_lbl = font_small.render("SPEED (KM/H)", True, TEXT_DIM)
        text_speed = font_large.render(f"{wheel_speed_kmh:03d}", True, TEXT_MAIN)
        screen.blit(text_speed_lbl, (550, 50))
        screen.blit(text_speed, (550, 80))

        # Pedals
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