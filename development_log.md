# Geliştirme Günlüğü (Development Log) - Dirt Rally Projesi
*Son Güncelleme: [17.04.2026]*


Bu dosya, DiRT Rally 2.0 özel telemetri analiz aracı ve gösterge paneli projesinin gelişim sürecini takip etmek amacıyla oluşturulmuştur.

## 🏁 Mevcut Durum Özeti
Proje, oyun motoru tarafından 60Hz hızında yayınlanan ham UDP paketlerini (Extradata=3 formatı) yakalayıp gerçek zamanlı olarak işleyebilecek seviyeye gelmiştir. Hem yazılımsal arayüzler hem de donanımsal geri bildirim (LED) mekanizmaları kurulmuştur. Oyun Windows 11 üzerinde çalışıyor, göstergeyi ise RPi5'ten çizdiriyoruz.

---

## 🛠 Tamamlanan Çalışmalar

### 1. Veri Altyapısı ve İletişim
- **UDP Dinleyici:** `socket` kütüphanesi kullanılarak oyunun gönderdiği 264 bytelık paketleri yakalayan yapı kuruldu.
- **Veri Ayrıştırma (Parsing):** `struct.unpack` ile ham veriler; hız, RPM, vites, pedal basınçları ve tekerlek hızları gibi anlamlı değişkenlere dönüştürüldü.
- **Konfigürasyon Sistemi:** `config.py` üzerinden IP, port ve LED aktivasyon ayarları merkezi hale getirildi.

### 2. Dijital Gösterge Paneli (digital_dash.py) - *En Kararlı Sürüm*
- **Arayüz Tasarımı:** Modern, koyu temalı bir dashboard oluşturuldu.
- **RPM Çubuğu:** RPM oranına göre renk değiştiren (normal/uyarı) dinamik bir bar yapıldı.
- **Çekiş Kaybı (Traction Loss) Uyarı Sistemi:** Tekerlek hızı ile araç hızı arasındaki fark hesaplanarak "SLIP" uyarısı veren bir algoritma eklendi.
- **Pedal Takibi:** Gaz ve fren girişleri için dikey görsel barlar eklendi.

### 3. Donanım Entegrasyonu (led_controller.py)
- **Raspberry Pi Desteği:** `gpiozero` kütüphanesi kullanılarak fiziksel LED'lerin (Yeşil, Mavi, Kırmızı) RPM oranına göre yanması sağlandı.
- **Geri Bildirim:** Yazılımdaki devir bilgisiyle senkronize çalışan bir vites değişim ışığı (Shift Light) sistemi simüle edildi.

### 4. Analog Gösterge Paneli (analog_dash.py) - *İlk Aşama*
- **Geometrik Hesaplamalar:** Trigonometrik fonksiyonlar (`math.sin`, `math.cos`) kullanılarak analog bir devir saati ve hareketli ibne mekanizması oluşturuldu.
- **Merkezi Vites Göstergesi:** Kadranın ortasına büyük bir vites göstergesi yerleştirildi.

---

## 🚀 Gelecek Hedefler ve İyileştirmeler

- **Analog Gösterge İyileştirmesi:** Şu an temel seviyede olan analog göstergenin görsel kalitesi artırılacak. İğne hareketi daha akıcı (smooth) hale getirilecek ve kadran üzerine numerik RPM değerleri eklenecek.
- **Loglama Sistemi:** Telemetri verilerinin analiz için bir dosyaya (CSV veya JSON) kaydedilmesi sağlanacak.
- **Yerel Çalışan Gösterge:** Oyunun çalıştığı bilgisayarda oyun pencere modunda açıkken ekranın alt kısmında çalışacak bir gösterge oluşturulacak (Windows ve Linux için).
- **Performans Optimizasyonu:** UDP paket işleme sırasındaki gecikmeleri (latency) minimize etmek için tampon bellek yönetimi geliştirilecek.

---
