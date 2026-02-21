import socket
import struct
import pygame
import sys

# --- 1. UDP AĞ AYARLARI ---
LISTEN_IP = "0.0.0.0"
LISTEN_PORT = 20777
# UDP soketi oluşturulur (IPv4 ve Datagram mantığı)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LISTEN_IP, LISTEN_PORT))
# Timeout değeri 0.01 saniye (10 ms) olarak ayarlanır. Bu, havuz boşaltma tekniğinin çalışması için şarttır.
sock.settimeout(0.01)

# --- 2. PYGAME ARAYÜZ AYARLARI ---
pygame.init()
WIDTH, HEIGHT = 800, 480 
ekran = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RALLİ TELEMETRİ İSTASYONU")

# Renk Paleti (RGB Formatında)
SIYAH = (10, 10, 10)
YESIL = (0, 255, 0)
TURUNCU = (255, 176, 0)
KIRMIZI = (255, 0, 0)
BEYAZ = (200, 200, 200)

# Arayüz Fontları
font_buyuk = pygame.font.SysFont("monospace", 48, bold=True)
font_orta = pygame.font.SysFont("monospace", 36, bold=True)
font_kucuk = pygame.font.SysFont("monospace", 24)

# Değişkenlerin ilk değer atamaları
teker_hizi_kmh = 0
devir = 0
max_devir = 8000 
vites_str = "N"

# 60 FPS sabitleyici nesne
saat = pygame.time.Clock() 

# --- 3. ANA ÇİZİM VE HESAPLAMA DÖNGÜSÜ ---
while True:
    # A. İşletim Sistemi Olayları (Kapatma butonuna basıldı mı?)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            sys.exit() 

    # B. Veri Dinleme (Havuz Boşaltma / Buffer Draining Algoritması)
    son_paket = None
    try:
        # Kuyruktaki tüm paketleri tükenene kadar hızlıca oku
        while True:
            data, addr = sock.recvfrom(1024)
            if len(data) == 264:
                son_paket = data # Sadece en son gelen (en güncel) paketi sakla
    except socket.timeout:
        # Kuyruk boşaldığında timeout tetiklenir ve döngüden çıkılır, çizime devam edilir
        pass 

    # Eğer en az bir taze paket yakalandıysa verileri ayrıştır
    if son_paket:
        # 264 bytelık veri, 66 adet ondalıklı sayıya (float) çevrilir
        veriler = struct.unpack('66f', son_paket)
        
        # 4 Tekerleğin hız indeksleri: 25(Arka Sol), 26(Arka Sağ), 27(Ön Sol), 28(Ön Sağ)
        # Çekiş sisteminden bağımsız (FWD, RWD, AWD) stabil veri için 4 tekerleğin ortalaması alınır
        teker_hizi_ms = (veriler[25] + veriler[26] + veriler[27] + veriler[28]) / 4
        teker_hizi_kmh = int(teker_hizi_ms * 3.6) # m/s değerini km/h formatına dönüştür
        
        # Devir verileri indeks 37 ve 63'te bulunur (Gerçek değer için 10 ile çarpılmalıdır)
        devir = int(veriler[37] * 10)
        okunan_max_devir = int(veriler[63] * 10)
        
        # Oyun başlangıcında max_devir 0 gelebilir, sıfıra bölünme hatasını önlemek için kontrol edilir
        if okunan_max_devir > 0:
            max_devir = okunan_max_devir
        
        # Vites verisi indeks 33'tedir.
        vites = int(veriler[33])
        if vites == 0: vites_str = "N" # Boş Vites
        elif vites == 10: vites_str = "R" # Geri Vites
        else: vites_str = str(vites)

    # C. Grafiklerin Çizilmesi
    ekran.fill(SIYAH) # Her karede ekranı temizle
    
    # Üst Bilgi Başlığı
    yazi_baslik = font_kucuk.render("SİSTEM: DIRT RALLY 2.0 BAĞLANTISI AKTİF", True, TURUNCU)
    ekran.blit(yazi_baslik, (20, 20))
    pygame.draw.line(ekran, TURUNCU, (20, 50), (WIDTH - 20, 50), 2)
    
    # Hız ve Vites Göstergeleri
    yazi_hiz = font_buyuk.render(f"HIZ  : {teker_hizi_kmh:03d} KM/H", True, YESIL)
    ekran.blit(yazi_hiz, (50, 100))
    
    yazi_vites = font_buyuk.render(f"VİTES: {vites_str}", True, YESIL)
    ekran.blit(yazi_vites, (50, 180))

    # --- Devir Çubuğu (RPM Bar) ---
    bar_max_genislik = 600 
    bar_yukseklik = 40
    bar_x = 50 
    bar_y = 300 
    
    # Çubuğun doluluk oranı hesaplanır
    oran = devir / max_devir
    # Taşkınlıkları (örneğin devir kesiciye girildiğinde) önlemek için oran 0.0 ile 1.0 arasına hapsedilir
    if oran > 1.0: oran = 1.0 
    if oran < 0.0: oran = 0.0
    
    bar_guncel_genislik = int(bar_max_genislik * oran)
    
    # Vites büyütme uyarısı (%90 doluluğa ulaşıldığında)
    if oran >= 0.90:
        bar_renk = KIRMIZI 
        yazi_uyari = font_orta.render("VİTES YÜKSELT!", True, KIRMIZI) 
        ekran.blit(yazi_uyari, (bar_x + bar_max_genislik + 20, bar_y)) 
    else:
        bar_renk = YESIL 
        
    # İçi dolu devir seviyesi çizilir
    pygame.draw.rect(ekran, bar_renk, (bar_x, bar_y, bar_guncel_genislik, bar_yukseklik))
    # Dış çerçeve çizilir (Son parametre olan 3, çizgi kalınlığıdır)
    pygame.draw.rect(ekran, BEYAZ, (bar_x, bar_y, bar_max_genislik, bar_yukseklik), 3)
    
    # Çubuğun üstüne rakamsal devir değerleri eklenir
    yazi_rpm = font_kucuk.render(f"{devir} / {max_devir} RPM", True, BEYAZ)
    ekran.blit(yazi_rpm, (bar_x, bar_y - 30))

    # D. Hazırlanan Kareyi Monitöre Gönder
    pygame.display.flip() 
    saat.tick(60) # Döngüyü 60 FPS'e sabitle