# Changelog

Bu dosyada yalnızca **dosya başlıkları** altında yapılan değişiklikler özetlenir.
Hedefler buraya yazılmaz — bkz. `ROADMAP.md`. Mimari açıklamalar için bkz.
`ARCHITECTURE.md`. Eski serbest metin günlüğü, kişisel arşiv olarak
`development_log.md` içinde (git'te izlenmez) tutulur.

> CHANGELOG.md'ye değişiklikler yazılırken her zaman en üstteki "## Son Değişiklikler" başlığı altına ("Son değişiklikler" başlığı altındaki önceki metin "geçmiş değişiklikler" başlığı altına düzeni bozmayacak şekilde taşınarak), "### dosya_adı.x" alt başlığıyla liste olarak eklenecek.

## Son Değişiklikler

### .gitattributes / install.bat / run_dash.bat / check_telemetry.bat
- `.gitattributes`: Repodaki `.bat` ve `.cmd` dosyalarının Git ve ZIP arşivleme işlemlerinde her zaman `CRLF` satır sonuna sahip olmasını sağlayan yapılandırma eklendi.
- `install.bat`, `run_dash.bat`, `check_telemetry.bat`: Unix `LF` satır sonlarında `cmd.exe` parantez bloğu sözdizimi çökmesini önlemek amacıyla çok satırlı `if (...)` blokları `goto` ve etiket tabanlı akışa dönüştürüldü; olası hata durumlarında pencerenin kapanması engellendi.

---

## Geçmiş değişiklikler

### setup_wizard.py / install.bat / run_dash.bat / check_telemetry.bat / telemetry_check.py
- `setup_wizard.py`: İki dilli (İngilizce ve Türkçe) ilk kurulum desteği eklendi; başlangıçta dil seçimi (`en`/`tr`) soruluyor, Türkçe metinlerde UTF-8 karakterler eksiksiz kullanıldı.
- `install.bat` & `run_dash.bat`: Terminal çıktıları İngilizceye çevrilerek standartlaştırıldı; adımlar `[1/3]`, `[2/3]`, `[3/3]` şeklinde satır boşluklarıyla ayrıldı ve kurulum sonu mükerrer bildirimler kaldırıldı.
- `check_telemetry.bat`: Windows ortamında sanal ortam üzerinden `telemetry_check.py`'yi tek tıkla çalıştıran yeni yardımcı betik eklendi.
- `telemetry_check.py`: Konsol hata ve durum mesajları İngilizce olarak standartlaştırıldı.
- Kurulum sonu özetinde `telemetry_check` teşhis adımı ve sanal ortam çalıştırma komutları belirginleştirildi.

### Kurulum ve dokümantasyon
- Windows için Python 3.12 sanal ortamı oluşturan `install.bat` ve dashboard'u başlatan `run_dash.bat` eklendi.
- `setup_wizard.py` eklendi; `config.py` ve DiRT Rally 2.0 telemetry XML'i yedeklenerek güncelleniyor.
- Kurulumda alıcı IP adresi soruluyor; `127.0.0.1` loopback/Firewall uyarısı ile varsayılan olarak sunuluyor.
- Windows ve Raspberry Pi bağımlılıkları ayrıldı; Python sürümü 3.12 ile sınırlandırıldı.
- README, CONFIGURATION ve ARCHITECTURE kurulum akışına göre güncellendi.

### docs
- Geçmiş temizliği (`git filter-repo`): `venv/` dizini tüm commit geçmişinden kaldırıldı; yazar/committer kimliği `alpivenator` + GitHub noreply e-postasına sabitlendi; `origin` URL'si yeni hesaba güncellendi (repo boyutu ~14 MiB → ~353 KiB).
- `ROADMAP.md`: tamamlanan "Hassas veri taraması" maddesi kaldırıldı; Not metnindeki ifade düzeltildi ("hedefler yöneticinin isteğiyle güncellenir").

### settings.py / digital_dash.py / analogdash.py
- Pencere boyutları `settings.py`'deki `DIGITAL_WIDTH/HEIGHT` ve `ANALOG_WIDTH/HEIGHT` ayarlarına bağlandı (`_BASE_W`, `_BASE_H` sabit değerleri kaldırıldı). Varsayılanlar aynı kaldığı için görsel değişiklik yok.

### ARCHITECTURE.md
- `analogdash.py` açıklamasındaki yanlış boyut düzeltildi: 700×350 → 600×350.

### LICENSE
- GPL-3.0 lisansı eklendi (telif: Alperen (alpivenator), 2026).

### pyproject.toml
- `[project]` metadata eklendi: `name = "dirtdash"`, `version = "0.1.0a1"`, `license = "GPL-3.0-only"`, `requires-python = ">=3.12"`; gpiozero `optional-dependencies`'e taşındı. Mevcut `[tool.black]` / `[tool.ruff]` korundu.

### CONFIG.md → CONFIGURATION.md
- Dosya `git mv` ile yeniden adlandırıldı.
- İngilizce kapsamlı ayar dokümantasyonu yazıldı: `config.py` (sistem) ve `settings.py` (görsel) tabloları, mevcut `0.0.0.0` açıklaması çevrilerek korundu, "Security Notes" bölümü eklendi.

### README.md
- Genişletildi: özellikler, gereksinimler, "3 adımda başlangıç", yapılandırma ve lisans bölümleri; ekran görüntüsü için placeholder eklendi.

---

## Geçmiş değişiklikler

`development_log.md` içindeki tamamlanmış maddelerden, dosya / alan bazında
yoğunlaştırılmış özet. Tam anlatı arşivde duruyor.

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
