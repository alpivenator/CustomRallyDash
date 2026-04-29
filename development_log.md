# Geliştirme Günlüğü (Development Log) - Dirt Rally Projesi
*Son Güncelleme: 20.04.2026*

# Dosyanın özeti
Bu dosya, Dirt Rally 2.0 özel telemetri analiz aracı ve gösterge paneli projesinin gelişim sürecini takip etmek amacıyla oluşturulmuştur.

## 🏁 Projenin Özeti
Proje, oyun motoru tarafından 60Hz hızında yayınlanan ham UDP paketlerini (Extradata=3 formatı) yakalayıp gerçek zamanlı olarak işleyebilecek seviyeye gelmiştir. Oyun Windows 11 üzerinde çalışırken, gösterge paneli bir Raspberry Pi 5 üzerinden çizdirilmektedir.

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
- [X] **Devir Okunurluğunu Artırma:** Numerik RPM etiketlerinin okunurluğu artıralacak.
- [x] **Sabit Ölçekli (0-9k) Gösterge:** RPM etiketleri GAUGE_MAX_RPM=9000 sabitine göre çizilir. 
- [x] **Kırmızı bölge:** Kırmızı bölge ve iğne rengi eşiği aracın gerçek max_rpm değerine göre dinamik olarak ayarlanacak. Kırmızı bölge, aracın maksimum devrinden başlayıp göstergenin maksimum devrinde bitecek.
- [ ] **Güzel ve Çekici Görünüm Verme:** Estetik pivot noktası, geliştirilmiş renk paleti ve merkezi vites dairesi.

### 5. Yerelde Çalıştırma
- [ ] **Windows Overlay Modu:** Oyun ekranının üzerinde çalışacak şeffaf overlay tasarımı.

## 🚀 Diğer Hedefler ve İyileştirmeler

- [ ] **Yerel Çalışan Gösterge:** Windows üzerinde oyun açıkken ekranın altında çalışacak overlay modu. **[Önem: 5/5]**
- [ ] **Performans Optimizasyonu:** UDP paket işleme gecikmelerini (latency) düşürmek için buffer yönetimi. **[Önem: 5/5]**
- [ ] **Özelleştirilebilirlik:** Modüler kod yapısı ile kullanıcı dostu arayüz ayarları. **[Önem: 4/5]**
- [ ] **Günlükleme Sistemi:** Analiz için telemetri verilerinin CSV/JSON formatında kaydedilmesi. **[Önem: 2/5]**

---
