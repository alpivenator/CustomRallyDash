import socket
import struct
import pygame
import sys
# YENİ: GPIO kontrol kütüphanesi
from gpiozero import LED

# --- 1. UDP AĞ AYARLARI ---
LISTEN_IP = "0.0.0.0"
LISTEN_PORT = 20777
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LISTEN_IP, LISTEN_PORT))
sock.settimeout(0.01)

# --- 2. DONANIM (LED) AYARLARI ---
# Yeni pin numaraları GPIO numaralarıdır (Fiziksel pin sırası değil).
# Fiziksel takıp çıkarma kolaylığı için kartın en uç kısmındaki pinler seçilmiştir.
led_yesil = LED(16)
led_mavi = LED(20)
led_kirmizi = LED(21)

# Başlangıçta tüm ledleri söndür
led_yesil.off()
led_mavi.off()
led_kirmizi.off()

# --- 3. PYGAME ARAYÜZ AYARLARI ---
pygame.init()
WIDTH, HEIGHT = 800, 400 
ekran = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MODERN RALLİ TELEMETRİSİ")

ARKA_PLAN = (25, 25, 30)
METIN_ANA = (240, 240, 240)
METIN_PASIF = (120, 120, 130)
DEVIR_NORMAL = (0, 150, 255)
DEVIR_UYARI = (255, 40, 40)
GAZ_RENK = (40, 220, 100)
FREN_RENK = (255, 60, 60)
CERCEVE = (80, 80, 90)
PATINAJ_RENK = (255, 200, 0)

font_dev = pygame.font.SysFont("arial", 72, bold=True)
font_buyuk = pygame.font.SysFont("arial", 48, bold=True)
font_orta = pygame.font.SysFont("arial", 32, bold=True)
font_kucuk = pygame.font.SysFont("arial", 20)

teker_hizi_kmh = 0
arac_hizi_kmh = 0 
devir = 0
max_devir = 8000 
vites_str = "N"
gaz_pedal = 0.0
fren_pedal = 0.0

saat = pygame.time.Clock() 

# --- 4. ANA DÖNGÜ ---
# Program kapanırken LED'leri temizlemek için try-finally bloğu kullanıyoruz
try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                sys.exit() 

        son_paket = None
        try:
            while True:
                data, addr = sock.recvfrom(1024)
                if len(data) == 264:
                    son_paket = data
        except socket.timeout:
            pass 

        if son_paket:
            veriler = struct.unpack('66f', son_paket)
            arac_hizi_kmh = int(veriler[7] * 3.6) 
            teker_hizi_ms = (veriler[25] + veriler[26] + veriler[27] + veriler[28]) / 4
            teker_hizi_kmh = int(teker_hizi_ms * 3.6) 
            
            devir = int(veriler[37] * 10)
            okunan_max_devir = int(veriler[63] * 10)
            if okunan_max_devir > 0: max_devir = okunan_max_devir
            
            vites = int(veriler[33])
            if vites == 0: vites_str = "N" 
            elif vites == 10: vites_str = "R" 
            else: vites_str = str(vites)
                
            gaz_pedal = veriler[29]
            fren_pedal = veriler[31]

        ekran.fill(ARKA_PLAN) 
        
        yazi_vites_etiket = font_kucuk.render("VİTES", True, METIN_PASIF)
        yazi_vites = font_dev.render(vites_str, True, METIN_ANA)
        ekran.blit(yazi_vites_etiket, (50, 100))
        ekran.blit(yazi_vites, (50, 120))

        yazi_hiz_etiket = font_kucuk.render("HIZ (KM/H)", True, METIN_PASIF)
        yazi_hiz = font_dev.render(f"{teker_hizi_kmh:03d}", True, METIN_ANA)
        ekran.blit(yazi_hiz_etiket, (250, 100))
        ekran.blit(yazi_hiz, (250, 120))

        bar_x, bar_y = 50, 40
        bar_max_w, bar_h = 700, 30
        
        oran = devir / max_devir
        if oran > 1.0: oran = 1.0 
        if oran < 0.0: oran = 0.0
        
        bar_guncel_w = int(bar_max_w * oran)
        
        # --- YENİ: FİZİKSEL LED KONTROLÜ MANTIĞI ---
        # Oran %80'i geçerse Yeşil yanar
        if oran >= 0.76: led_yesil.on()
        else: led_yesil.off()
        
        # Oran %88'i geçerse Mavi de yanar
        if oran >= 0.85: led_mavi.on()
        else: led_mavi.off()
        
        # Oran %95'i geçerse Kırmızı da yanar (Vites At) ve Ekranda bar kırmızı olur
        if oran >= 0.90: 
            led_kirmizi.on()
            bar_renk = DEVIR_UYARI
        else: 
            led_kirmizi.off()
            bar_renk = DEVIR_NORMAL
            
        pygame.draw.rect(ekran, bar_renk, (bar_x, bar_y, bar_guncel_w, bar_h))
        pygame.draw.rect(ekran, CERCEVE, (bar_x, bar_y, bar_max_w, bar_h), 2)
        
        yazi_rpm = font_orta.render(f"{devir} RPM", True, METIN_ANA)
        ekran.blit(yazi_rpm, (WIDTH - 200, 80))

        if (teker_hizi_kmh - arac_hizi_kmh) > 20 and gaz_pedal > 0.5:
            pygame.draw.rect(ekran, PATINAJ_RENK, (450, 120, 120, 35))
            yazi_patinaj = font_kucuk.render("PATİNAJ", True, ARKA_PLAN)
            ekran.blit(yazi_patinaj, (470, 125))

        pedal_w, pedal_max_h = 40, 150
        fren_x, fren_y = 600, 150
        gaz_x, gaz_y = 670, 150
        
        if gaz_pedal > 1.0: gaz_pedal = 1.0
        if gaz_pedal < 0.0: gaz_pedal = 0.0
        if fren_pedal > 1.0: fren_pedal = 1.0
        if fren_pedal < 0.0: fren_pedal = 0.0

        gaz_h = int(pedal_max_h * gaz_pedal)
        fren_h = int(pedal_max_h * fren_pedal)

        pygame.draw.rect(ekran, FREN_RENK, (fren_x, fren_y + (pedal_max_h - fren_h), pedal_w, fren_h))
        pygame.draw.rect(ekran, CERCEVE, (fren_x, fren_y, pedal_w, pedal_max_h), 2)
        ekran.blit(font_kucuk.render("FRN", True, METIN_PASIF), (fren_x, fren_y + pedal_max_h + 10))

        pygame.draw.rect(ekran, GAZ_RENK, (gaz_x, gaz_y + (pedal_max_h - gaz_h), pedal_w, gaz_h))
        pygame.draw.rect(ekran, CERCEVE, (gaz_x, gaz_y, pedal_w, pedal_max_h), 2)
        ekran.blit(font_kucuk.render("GAZ", True, METIN_PASIF), (gaz_x, gaz_y + pedal_max_h + 10))

        pygame.display.flip() 
        saat.tick(60)
        
finally:
    # Program herhangi bir sebeple çökerse veya kapanırsa LED'leri söndür
    led_yesil.off()
    led_mavi.off()
    led_kirmizi.off()