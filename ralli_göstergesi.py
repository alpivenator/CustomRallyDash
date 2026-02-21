import socket
import struct
import pygame
import sys

# --- 1. UDP AĞ AYARLARI ---
LISTEN_IP = "0.0.0.0"
LISTEN_PORT = 20777
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LISTEN_IP, LISTEN_PORT))
sock.settimeout(0.01)

# --- 2. PYGAME ARAYÜZ VE RENK AYARLARI ---
pygame.init()
WIDTH, HEIGHT = 800, 440 
ekran = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MODERN RALLİ TELEMETRİSİ")

# Modern Yarış Paleti
ARKA_PLAN = (25, 25, 30)       # Koyu Karbon/Asfalt Grisi
METIN_ANA = (240, 240, 240)    # Temiz Beyaz
METIN_PASIF = (120, 120, 130)  # Soluk Gri (Önemsiz detaylar için)
DEVIR_NORMAL = (0, 150, 255)   # Modern Mavi
DEVIR_UYARI = (255, 40, 40)    # Canlı Kırmızı
GAZ_RENK = (40, 220, 100)      # Canlı Yeşil
FREN_RENK = (255, 60, 60)      # Canlı Kırmızı
CERCEVE = (80, 80, 90)         # Koyu Gri Çerçeveler

font_dev = pygame.font.SysFont("arial", 72, bold=True)
font_buyuk = pygame.font.SysFont("arial", 48, bold=True)
font_orta = pygame.font.SysFont("arial", 32, bold=True)
font_kucuk = pygame.font.SysFont("arial", 20)

# Başlangıç Değerleri
teker_hizi_kmh = 0
devir = 0
max_devir = 8000 
vites_str = "N"
gaz_pedal = 0.0  # 0.0 ile 1.0 arası
fren_pedal = 0.0 # 0.0 ile 1.0 arası

saat = pygame.time.Clock() 

# --- 3. ANA DÖNGÜ ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            sys.exit() 

    # Havuz Boşaltma (Buffer Draining)
    son_paket = None
    try:
        while True:
            data, addr = sock.recvfrom(1024)
            if len(data) == 264:
                son_paket = data
    except socket.timeout:
        pass 

    # Veri Ayrıştırma
    if son_paket:
        veriler = struct.unpack('66f', son_paket)
        
        # 4 Tekerlek Ortalaması (İndeks 25, 26, 27, 28)
        teker_hizi_ms = (veriler[25] + veriler[26] + veriler[27] + veriler[28]) / 4
        teker_hizi_kmh = int(teker_hizi_ms * 3.6) 
        
        devir = int(veriler[37] * 10)
        okunan_max_devir = int(veriler[63] * 10)
        if okunan_max_devir > 0: max_devir = okunan_max_devir
        
        vites = int(veriler[33])
        if vites == 0: vites_str = "N" 
        elif vites == 10: vites_str = "R" 
        else: vites_str = str(vites)
            
        # Gaz ve Fren Pedalı (0.0 ile 1.0 arası gelir)
        gaz_pedal = veriler[29]
        fren_pedal = veriler[31]

    # --- GRAFİK ÇİZİMİ ---
    ekran.fill(ARKA_PLAN) 
    
    # 1. Hız ve Vites (Sol Orta)
    yazi_vites_etiket = font_kucuk.render("VİTES", True, METIN_PASIF)
    yazi_vites = font_dev.render(vites_str, True, METIN_ANA)
    ekran.blit(yazi_vites_etiket, (50, 100))
    ekran.blit(yazi_vites, (50, 120))

    yazi_hiz_etiket = font_kucuk.render("HIZ (KM/H)", True, METIN_PASIF)
    yazi_hiz = font_dev.render(f"{teker_hizi_kmh:03d}", True, METIN_ANA)
    ekran.blit(yazi_hiz_etiket, (250, 100))
    ekran.blit(yazi_hiz, (250, 120))

    # 2. Devir Çubuğu (Üst Kısım - Yatay)
    bar_x, bar_y = 50, 40
    bar_max_w, bar_h = 700, 30
    
    oran = devir / max_devir
    if oran > 1.0: oran = 1.0 
    if oran < 0.0: oran = 0.0
    
    bar_guncel_w = int(bar_max_w * oran)
    bar_renk = DEVIR_UYARI if oran >= 0.90 else DEVIR_NORMAL
        
    pygame.draw.rect(ekran, bar_renk, (bar_x, bar_y, bar_guncel_w, bar_h))
    pygame.draw.rect(ekran, CERCEVE, (bar_x, bar_y, bar_max_w, bar_h), 2)
    
    yazi_rpm = font_orta.render(f"{devir} RPM", True, METIN_ANA)
    ekran.blit(yazi_rpm, (WIDTH - 200, 80))

    # 3. Gaz ve Fren Çubukları (Sağ Alt - Dikey)
    pedal_w, pedal_max_h = 40, 150
    fren_x, fren_y = 600, 150
    gaz_x, gaz_y = 670, 150
    
    # Veri sapmalarını engellemek için sınırlandırma
    if gaz_pedal > 1.0: gaz_pedal = 1.0
    if gaz_pedal < 0.0: gaz_pedal = 0.0
    if fren_pedal > 1.0: fren_pedal = 1.0
    if fren_pedal < 0.0: fren_pedal = 0.0

    # Dikey barlar aşağıdan yukarıya dolar. PyGame'de Y ekseni yukarıdan aşağı artar.
    # Bu yüzden çizime (Y + Max Yükseklik - Güncel Yükseklik) noktasından başlarız.
    gaz_h = int(pedal_max_h * gaz_pedal)
    fren_h = int(pedal_max_h * fren_pedal)

    # Fren Çizimi
    pygame.draw.rect(ekran, FREN_RENK, (fren_x, fren_y + (pedal_max_h - fren_h), pedal_w, fren_h))
    pygame.draw.rect(ekran, CERCEVE, (fren_x, fren_y, pedal_w, pedal_max_h), 2)
    ekran.blit(font_kucuk.render("FRN", True, METIN_PASIF), (fren_x, fren_y + pedal_max_h + 10))

    # Gaz Çizimi
    pygame.draw.rect(ekran, GAZ_RENK, (gaz_x, gaz_y + (pedal_max_h - gaz_h), pedal_w, gaz_h))
    pygame.draw.rect(ekran, CERCEVE, (gaz_x, gaz_y, pedal_w, pedal_max_h), 2)
    ekran.blit(font_kucuk.render("GAZ", True, METIN_PASIF), (gaz_x, gaz_y + pedal_max_h + 10))

    pygame.display.flip() 
    saat.tick(60)