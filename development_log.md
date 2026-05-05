# Geliştirme Günlüğü (Development Log) - Dirt Rally Projesi
*Son Güncelleme: 01.05.2026*

# Dosyanın özeti
Bu dosya, Dirt Rally 2.0 özel telemetri analiz aracı ve gösterge paneli projesinin gelişim sürecini takip etmek amacıyla oluşturulmuştur.

## 🏁 Projenin Özeti
Proje, oyun motoru tarafından 60Hz hızında yayınlanan ham UDP paketlerini (Extradata=3 formatı) yakalayıp gerçek zamanlı olarak işlemektedir. Öncelikli hedef, Windows üzerinde oyunla birlikte yerel çalışan, kullanıcı tarafından özelleştirilebilen bir overlay gösterge panelidir.

---

## 🛠 Tamamlanan ve Tamamlanacak Çalışmalar

### 1. Veri Altyapısı ve İletişim
- [x] **UDP Dinleyici:** `socket` kütüphanesi ile 264 bytelık paketleri yakalayan altyapı.
- [x] **Veri Ayrıştırma (Parsing):** `struct.unpack` ile hız, RPM, vites ve pedal verilerinin decode edilmesi.
- [x] **Konfigürasyon Sistemi:** `config.py` ile merkezi IP/Port ve donanım ayarları.

### 2. Dijital Gösterge Paneli (digital_dash.py)
- [x] **Arayüz Tasarımı:** Modern ve okunaklı koyu tema tasarımı.
- [x] **Dinamik RPM Barı:** Devir oranına göre renk değiştiren gösterge.
- [x] **SLIP Uyarı Sistemi:** Tekerlek ve araç hızı farkına dayalı çekiş kaybı algoritması.
- [x] **Pedal Takibi:** Gaz ve fren girişleri için anlık dikey barlar.
- [x] **Kompakt Tasarım:** Pencere boyutu küçültülerek (600x300) daha minimal ve overlay için uygun hale getirildi.
- [x] **WRC/F1 Tarzı Tasarım:** Patinaj bilgisi kaldırıldı, hız ortalandı, pedal çubukları yatay hale getirildi, gösterge daha da kısaltıldı (600x200).

### 3. Donanım Entegrasyonu (led_controller.py)
- [x] **RPi GPIO Desteği:** `gpiozero` ile fiziksel LED kontrolü.
- [x] **Shift Light Sistemi:** RPM oranına bağlı Yeşil-Mavi-Kırmızı vites değişim ışıkları.

### 4. Analog Gösterge Paneli (analog_dash.py) 
- [x] **Geometrik İğne Mekanizması:** Trigonometrik hesaplamalarla çalışan analog kadran.
- [x] **İğne Yumuşatma (Smoothing):** Linear interpolation ile akıcı iğne hareketi.
- [x] **Detaylı Kadran Tasarımı:** Ana ve ara RPM işaretçileri (Ticks).
- [x] **Redline Vurgusu:** Yarı saydam kırmızı tehlike bölgesi tasarımı.
- [x] **Devir Okunurluğunu Artırma:** Numerik RPM etiketlerinin okunurluğu artıralacak.
- [x] **Sabit Ölçekli (0-9k) Gösterge:** RPM etiketleri GAUGE_MAX_RPM=9000 sabitine göre çizilir. 
- [x] **Kırmızı bölge:** Kırmızı bölge ve iğne rengi eşiği aracın gerçek max_rpm değerine göre dinamik olarak ayarlanır. Kırmızı bölge, aracın maksimum devrinden başlayıp göstergenin maksimum devrinde biter.
- [ ] **Görsel İyileştirme:** Estetik pivot noktası, geliştirilmiş renk paleti ve merkezi vites dairesi.

### 5. Yerelde Çalıştırma ve Overlay (Öncelik: 1)
- [x] **Platform Tespit Altyapısı:** `sys.platform` ile Windows/Linux ayrımı yapılır. Overlay modülü yalnızca `win32` platformunda içe aktarılır.
- [x] **Windows Overlay Modülü (`overlay_win.py`):** `ctypes` ile Win32 API çağrıları bu modülde toplanır (taslak oluşturuldu).
  - [x] **Çerçevesiz Pencere:** `WS_POPUP` stili ile başlık çubuğu olmayan pencere.
  - [x] **Yarı Saydamlık:** `WS_EX_LAYERED` + `SetLayeredWindowAttributes` ile arka plan rengi anahtar renk olarak saydamlaştırılır.
  - [x] **Tıklama Geçirgenlik:** `WS_EX_TRANSPARENT` ile fare tıklamaları oyuna iletilir.
  - [x] **En Üstte Kalma:** `HWND_TOPMOST` ile `SetWindowPos` üzerinden always-on-top.
- [x] **Digital Dash Overlay Entegrasyonu:** `config.ENABLE_OVERLAY` true olduğunda digital_dash.py overlay ayarlarını uygular; konfigürasyon `config.py` üzerinden yapılır.
- [ ] **Windows Başlangıç Betiği:** Tek tıkla çalıştırma için `run_dash.bat` başlatıcı.

### 6. Özelleştirilebilirlik (Öncelik: 2)
- [ ] **Orantılı Ölçeklendirme:** Pencere boyutu değiştiğinde tüm içerik (yazılar, çubuklar, kadran) orantılı olarak ölçeklenir.
- [ ] **Renk Teması:** Tüm renkler `config.py` üzerinden değiştirilebilir.
- [ ] **Stil Seçimi:** Dijital veya analog gösterge arasında `config.py` üzerinden geçiş yapılabilir.

### 7. Mimari İyileştirmeler (Öncelik: 3)
- [ ] **Modüler UDP Modülü:** Ağ kodunun `udp_listener.py` adında ortak bir modüle taşınması.
- [ ] **Birleşik Çalıştırıcı:** `main.py` ile kullanıcı tercihine göre dijital/analog göstergeyi başlatan tek giriş noktası.
- [x] **Platform Soyutlama:** Overlay mantığı `overlay_win.py` modülünde izole edildi; Linux'ta bu modül atlanarak mevcut pygame penceresi kullanılır.

## 🚀 Diğer Hedefler ve İyileştirmeler

- [ ] **Performans Optimizasyonu:** UDP paket işleme gecikmelerini düşürmek için buffer yönetimi. **[Önem: 4/5]**
- [ ] **Günlükleme Sistemi:** Analiz için telemetri verilerinin CSV/JSON formatında kaydedilmesi. **[Önem: 2/5]**
- [ ] **Linux Overlay Desteği:** X11/Wayland üzerinde saydam overlay penceresi (ileri dönem). **[Önem: 1/5]**

