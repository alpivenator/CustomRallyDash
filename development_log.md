# Geliştirme Günlüğü (Development Log) - Dirt Rally Projesi
*Son Güncelleme: 17.04.2026*

# YZ talimatlarım
YZ modeli, bu metni otomatik güncellerken "Hedefler" kısmına rastgele yeni hedefler ekleme. O kısmı ben güncelleyeceğim.

Bu dosya, DiRT Rally 2.0 özel telemetri analiz aracı ve gösterge paneli projesinin gelişim sürecini takip etmek amacıyla oluşturulmuştur.

## 🏁 Mevcut Durum Özeti
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

### 3. Donanım Entegrasyonu (led_controller.py)
- [x] **RPi GPIO Desteği:** `gpiozero` ile fiziksel LED kontrolü.
- [x] **Shift Light Sistemi:** RPM oranına bağlı Yeşil-Mavi-Kırmızı vites değişim ışıkları.

### 4. Analog Gösterge Paneli (analog_dash.py) 
- [x] **Geometrik İğne Mekanizması:** Trigonometrik hesaplamalarla çalışan analog kadran.
- [x] **İğne Yumuşatma (Smoothing):** Linear interpolation ile akıcı iğne hareketi.
- [x] **Detaylı Kadran Tasarımı:** Ana ve ara RPM işaretçileri (Ticks).
- [x] **Redline Vurgusu:** Yarı saydam kırmızı tehlike bölgesi tasarımı.
- [ ] **Devir Okunurluğunu Artırma:** Numerik RPM etiketleri ve dijital RPM göstergesi eklenmesi.
- [ ] **Güzel ve Çekici Görünüm Verme:** Estetik pivot noktası, geliştirilmiş renk paleti ve merkezi vites dairesi.

---

## 🚀 Diğer Hedefler ve İyileştirmeler

- [ ] **Yerel Çalışan Gösterge:** Windows üzerinde oyun açıkken ekranın altında çalışacak overlay modu. **[Önem: 5/5]**
- [ ] **Performans Optimizasyonu:** UDP paket işleme gecikmelerini (latency) düşürmek için buffer yönetimi. **[Önem: 5/5]**
- [ ] **Özelleştirilebilirlik:** Modüler kod yapısı ile kullanıcı dostu arayüz ayarları. **[Önem: 4/5]**
- [ ] **Günlükleme Sistemi:** Analiz için telemetri verilerinin CSV/JSON formatında kaydedilmesi. **[Önem: 2/5]**

---

