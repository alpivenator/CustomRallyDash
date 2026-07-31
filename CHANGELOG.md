# Changelog

Bu dosyada yalnızca **dosya başlıkları** altında yapılan değişiklikler özetlenir.
Hedefler buraya yazılmaz — bkz. `ROADMAP.md`. Mimari açıklamalar için bkz.
`ARCHITECTURE.md`. Eski serbest metin günlüğü, kişisel arşiv olarak
`development_log.md` içinde (git'te izlenmez) tutulur.

> CHANGELOG.md'ye değişiklikler yazılırken her zaman en üstteki "## Son Değişiklikler" başlığı altına ("Son değişiklikler" başlığı altındaki önceki metin "geçmiş değişiklikler" başlığı altına düzeni bozmayacak şekilde taşınarak), "### dosya_adı.x" alt başlığıyla liste olarak eklenecek.

## Son Değişiklikler

### requirements.txt
- gpiozero'nun yalnızca Raspberry Pi'de fiziksel LED kontrolü (`led_controller.py`) için gerekli olduğu, Windows'ta gerekmediği yorumla belirtildi.

### pyproject.toml
- `.gitignore`'dan çıkarıldı (git'e alındı).
- Ruff uyarısı düzeltildi: `select` → `lint.select`. Yorumlar İngilizceye çevrildi.

### docs
- `ROADMAP.md` yeniden yapılandırıldı: Alfa süreci bölümü (Faz 0–3, mermaid) kaldırıldı, tüm hedefler 5 genel başlıkta birleştirildi.

### udp_listener.py
- `__init__` içine `settimeout(0.01)` nedeninin (60 FPS UI döngüsünü bloklamamak) kısa açıklaması eklendi.
- `receive()` drain döngüsüne, yalnızca **en son 264 byte** paketinin tutulduğunu ve uzunluk filtresinin nedenini açıklayan yorumlar eklendi.
- `_parse()` içinde: tekerlek hızı ortalaması, m/s → km/h dönüşümü, RPM `*10` ölçeklemesi, `max_rpm` 8000 fallback'i, vites eşlemesi (`-1`→`R`, `0`→`N`) ve throttle/brake clamp'inin nedeni kısa yorumlarla belirtildi.

### docs
- `ARCHITECTURE.md` (EN) eklendi — modül görevleri, çalışma akışı, veri akışı, platform notları.
- `CHANGELOG.md` (TR) eklendi — bu dosya.
- `ROADMAP.md` (TR) eklendi — kullanıcı tarafından güncellenen hedefler.
- `development_log.md` arşiv olarak işaretlendi ve `.gitignore` listesine alındı.

---

## Geçmiş değişiklikler

`development_log.md` içindeki tamamlanmış maddelerden, dosya / alan bazında
yoğunlaştırılmış özet. Tam anlatı arşivde duruyor.

### udp_listener.py / Veri altyapısı
- 264 bytelık UDP paketlerini dinleyen altyapı (`socket`).
- `struct.unpack` ile hız, RPM, vites, pedal verilerinin ayrıştırılması.
- `config.py` üzerinden merkezi IP/Port ve donanım ayarları.
- `udp_listener.py` ortak modülüne taşındı; `TelemetryData` namedtuple + `UDPListener` sınıfı ile tek giriş noktası.

### digital_dash.py
- Modern koyu temalı, okunaklı arayüz tasarımı.
- Devir oranına göre renk değiştiren dinamik RPM barı.
- Tekerlek/araç hız farkına dayalı SLIP (çekiş kaybı) uyarı sistemi.
- Gaz ve fren için anlık dikey/yatay pedal barları.
- WRC/F1 tarzı kompakt düzen: vites merkezde büyütüldü (64→80), hız sola taşındı, pedal çubukları yatay, pencere 600×200.
- `OVERLAY_MODE="alpha"` ile pencere seviyesinde yarı saydamlık; `OVERLAY_ALPHA` ile opaklık ayarı.
- `config.ENABLE_OVERLAY` üzerinden Windows overlay entegrasyonu.
- Overlay açıkken `pygame.event.get()` nadiren veren `SystemError` try/except ile yakalandı.

### analogdash.py
- Trigonometrik hesaplarla çalışan geometrik iğne mekanizması.
- Linear interpolation ile iğne yumuşatma (smoothing).
- Ana ve ara RPM işaretleri (ticks) ile detaylı kadran tasarımı.
- Yarı saydam kırmızı redline bölgesi.
- RPM etiketleri `GAUGE_MAX_RPM=9000` sabitine göre sabit ölçekli çizim.
- Kırmızı bölge eşiği aracın gerçek `max_rpm` değerine göre dinamik.
- `overlay_win` entegrasyonu (`config.ENABLE_OVERLAY` ile).
- Pencere 800×400 → 700×350; kadran merkezi (350, 170), yarıçap 140.
- Gaz/fren çubukları kadranın yanlarına, dijital hız iğne-boşluğuna taşındı.

### led_controller.py
- `gpiozero` ile RPi GPIO üzerinden fiziksel LED kontrolü.
- RPM oranına bağlı Yeşil → Mavi → Kırmızı vites değişim ışıkları (shift light).

### overlay_win.py
- `sys.platform` ile Windows/Linux ayrımı; overlay modülü sadece Windows'ta içe aktarılır.
- `ctypes` ile Win32 API çağrıları tek modülde toplandı.
- `WS_POPUP` çerçevesiz pencere.
- `WS_EX_LAYERED` + `SetLayeredWindowAttributes` ile yarı saydamlık (alpha & chroma modları).
- `WS_EX_TRANSPARENT` ile fare tıklamalarının oyuna geçirilmesi.
- `HWND_TOPMOST` + `SetWindowPos` ile always-on-top.
- `position_window()` ile sol alt / alt orta / sağ alt konumlandırma.

### config.py / settings.py / main.py
- `DASH_STYLE` ayarı (`"digital"` / `"analog"`) eklendi.
- `settings.py` renk/boyut/pozisyon için `config.py`'den ayrıldı.
- `TARGET_WIDTH` üzerinden orantılı ölçeklendirme (scale factor).
- Tüm renkler `settings.py` üzerinden değiştirilebilir.
- `main.py` `config.DASH_STYLE`'a göre dijital/analog gösterge seçer.
- Linux'ta `overlay_win` atlanır, mevcut pygame penceresi kullanılır.

### Performans
- UDP buffer yönetimi (drain-keep-latest deseni).
