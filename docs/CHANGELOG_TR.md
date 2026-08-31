# Changelog (Türkçe)

Bu dosyada projede yapılan değişiklikler ters kronolojik sırayla (en yeni en üstte) belgelenir.
Gelecekteki hedefler için bkz. `ROADMAP_TR.md`. Mimari açıklamalar için bkz. `ARCHITECTURE.md`.

## [2026-08-31]

### Düzeltildi
- `pyproject.toml`: Modül içe aktarmalarının (`tools`, `dashboards`, `core`) yerel ortamda ve CI süreçlerinde sorunsuz çözümlenmesi için `pythonpath = ["."]` ve `testpaths = ["tests"]` içeren `[tool.pytest.ini_options]` yapılandırması eklendi.
- `.github/workflows/ci.yml`: Test çalıştırma adımı çalıştırıcı ortamlarında tutarlı yürütme sağlamak adına `python -m pytest` komutuna uyarlandı.

---

## [2026-08-29]

### Değiştirildi
- `tools/mock_telemetry.py`: Telemetri simülasyon döngüsü 15 saniyeye ve modern WRC ivmelenme dinamiğine uyarlandı; 9 saniyede 1'den 6. vitese (vites başına 1.5 sn) çıkılarak 205 km/s son hıza ulaşılması sağlandı.
- `tools/mock_telemetry.py`: Vites yükseltme aşaması sıralı yarış şanzımanına (close-ratio sequential) uygun hale getirildi; 1. vites 2500 RPM'den kalkarken üst vites geçişlerinde devir düşüşü ~5800 RPM seviyesine çekildi.
- `tools/mock_telemetry.py`: 9-15 saniye frenaj döngüsüne kademeli vites düşürme (6->1), ECU otomatik ara gazı darbesi (auto-blip throttle pulse ~%50) ve devir eşleme (rev-matching ~6800 RPM sıçraması ve motor freni süzülmesi) eklendi.

### Düzeltildi
- `tools/mock_telemetry.py`: Sentetik sürüş döngüsünün frenleme fazı 1. vitese ve durma/rölantiye kadar indirilecek şekilde uyarlandı; 15 saniyelik döngü başa sararken yaşanan ani vites sıçraması düzeltildi.

---

## [2026-08-28]

### Eklendi
- `dashboards/themes.py`: Motor sporları ve simülasyon kültüründen esinlenilen 5 hazır renk teması eklendi (`modern_dark`, `subaru_classic`, `gt3_racing`, `night_neon`, `retro_amber`).
- `tools/theme_selector.py` & `select_theme.bat`: Kullanıcının `settings.py` dosyasını bozmadan hazır temalar arasında güvenle geçiş yapmasını sağlayan iki dilli (EN/TR) interaktif CLI aracı ve Windows başlatıcısı eklendi.
- `tools/mock_telemetry.py` & `run_mock.bat`: Oyunu açmadan 60 Hz frekansında Extradata=3 UDP paketleri üreten, hızlanma, vites geçişleri, sert fren ve viraj çıkışı simüle eden hafif mock telemetri üreteci eklendi.
- `main.py`: Tek komutla dashboard ve sahte telemetriyi birlikte başlatan `--mock` parametresi desteği eklendi (`python main.py --mock`).
- `.github/ISSUE_TEMPLATE/`: GitHub için `bug_report.yml` ve `feature_request.yml` şablonları eklendi.
- `tests/test_themes_and_mock.py`: Mock paket üretim doğrulaması ve tema uygulama işlevleri için birim testleri eklendi.

### Değiştirildi
- `dashboards/analog_dash.py`: Analog göstergede iğne, vites kutusu dairesi ve merkez pivot noktasının çizim katman hiyerarşisi modernize edildi.
- `README.md`, `ARCHITECTURE.md`, `ROADMAP.md`: Yeni tema sistemi, mock önizleme araçları ve güncellenen mimariyle uyumlu hale getirildi.

---

## [2026-08-20]

### Refaktör
- `core/`: Telemetri ve donanım/platform katmanı `core/` paketine taşındı (`core/udp_listener.py`, `core/overlay_win.py`, `core/led_controller.py`); `core/__init__.py` üzerinden temiz export'lar sağlandı.
- `dashboards/`: Gösterge panelleri `dashboards/` paketine taşındı (`dashboards/digital_dash.py`, `dashboards/analog_dash.py`); `analogdash.py` ismi `analog_dash.py` olarak normalize edildi.
- `tools/`: İlk kurulum ve teşhis araçları `tools/` paketine taşındı (`tools/setup_wizard.py`, `tools/telemetry_check.py`); `setup_wizard.py` kök `config.py` yolunu dinamik olarak çözecek şekilde güncellendi, `telemetry_check.py` doğrudan çalıştırıldığında `sys.path` üzerinden kökü tanıyacak şekilde ayarlandı.
- `main.py`: Gösterge çalıştırma içe aktarmaları `dashboards.digital_dash` ve `dashboards.analog_dash` yollarına güncellendi.
- `install.bat` & `check_telemetry.bat`: Başlatıcılar `tools\setup_wizard.py` ve `tools\telemetry_check.py` hedeflerine güncellendi.
- `tests/test_setup_wizard.py`: Birim testler `tools.setup_wizard` ve `tools.telemetry_check` modüllerine göre uyarlandı.
- Dokümantasyon (`ARCHITECTURE.md`, `CONFIGURATION.md`, `README.md`): Yeni modüler dizin mimarisi ve komut yollarına göre güncellendi.

---

## [2026-08-18]

### Eklendi
- `.gitattributes`: Repodaki `.bat` ve `.cmd` dosyalarının Git ve ZIP arşivleme işlemlerinde her zaman `CRLF` satır sonuna sahip olmasını sağlayan yapılandırma eklendi.

### Düzeltildi
- `install.bat`, `run_dash.bat`, `check_telemetry.bat`: Unix `LF` satır sonlarında `cmd.exe` parantez bloğu sözdizimi çökmesini önlemek amacıyla çok satırlı `if (...)` blokları `goto` ve etiket tabanlı akışa dönüştürüldü; olası hata durumlarında pencerenin aniden kapanması engellendi.

---

## [2026-08-16 – 2026-08-17]

### Eklendi
- `setup_wizard.py`: İki dilli (İngilizce ve Türkçe) ilk kurulum desteği eklendi; başlangıçta dil seçimi (`en`/`tr`) soruluyor, Türkçe metinlerde UTF-8 karakterler eksiksiz kullanıldı.
- `check_telemetry.bat`: Windows ortamında sanal ortam üzerinden `telemetry_check.py`'yi tek tıkla çalıştıran yeni yardımcı betik eklendi.

### Değiştirildi
- `install.bat` & `run_dash.bat`: Terminal çıktıları İngilizceye çevrilerek standartlaştırıldı; adımlar `[1/3]`, `[2/3]`, `[3/3]` şeklinde satır boşluklarıyla ayrıldı ve kurulum sonu mükerrer bildirimler kaldırıldı.
- `telemetry_check.py`: Konsol hata ve durum mesajları İngilizce olarak standartlaştırıldı.
- Kurulum sonu özetinde `telemetry_check` teşhis adımı ve sanal ortam çalıştırma komutları belirginleştirildi.

---

## [2026-08-15]

### Eklendi
- Windows için Python 3.12 sanal ortamı oluşturan `install.bat` ve dashboard'u başlatan `run_dash.bat` eklendi.
- `setup_wizard.py` eklendi; `config.py` ve DiRT Rally 2.0 telemetry XML'i yedeklenerek güncelleniyor. Kurulumda alıcı IP adresi soruluyor; `127.0.0.1` loopback/Firewall uyarısı ile varsayılan olarak sunuluyor.
- `AGENTS.md` proje talimat dosyası eklendi.

### Değiştirildi
- Proje dokümantasyonu `docs/` dizini altına taşındı.
- Windows ve Raspberry Pi bağımlılıkları ayrıldı; Python sürümü 3.12 ile sınırlandırıldı.
- `README.md`, `CONFIGURATION.md` ve `ARCHITECTURE.md` kurulum akışına göre güncellendi.

---

## [2026-08-13]

### Değiştirildi
- Geçmiş temizliği (`git filter-repo`): `venv/` dizini tüm commit geçmişinden kaldırıldı; yazar/committer kimliği `alpivenator` + GitHub noreply e-postasına sabitlendi; `origin` URL'si yeni hesaba güncellendi (repo boyutu ~14 MiB → ~353 KiB).
- `ROADMAP.md`: Tamamlanan "Hassas veri taraması" maddesi kaldırıldı; Not metnindeki ifade düzeltildi ("hedefler yöneticinin isteğiyle güncellenir").

---

## [2026-08-05]

### Eklendi
- `LICENSE`: GPL-3.0 lisansı eklendi (telif: Alperen (alpivenator), 2026).
- `pyproject.toml`: `[project]` metadata eklendi: `name = "dirtdash"`, `version = "0.1.0a1"`, `license = "GPL-3.0-only"`, `requires-python = ">=3.12"`; gpiozero `optional-dependencies`'e taşındı.

### Değiştirildi
- `settings.py` / `digital_dash.py` / `analog_dash.py`: Pencere boyutları `settings.py`'deki `DIGITAL_WIDTH/HEIGHT` ve `ANALOG_WIDTH/HEIGHT` ayarlarına bağlandı (`_BASE_W`, `_BASE_H` sabit değerleri kaldırıldı).
- `CONFIG.md` → `CONFIGURATION.md`: Dosya yeniden adlandırıldı; İngilizce kapsamlı ayar dokümantasyonu yazıldı: `config.py` (sistem) ve `settings.py` (görsel) tabloları, `0.0.0.0` açıklaması ve "Security Notes" bölümü eklendi.
- `README.md`: Özellikler, gereksinimler, "3 adımda başlangıç", yapılandırma ve lisans bölümleriyle genişletildi.

---

## [2026-07-14 – 2026-07-31]

### Eklendi
- `ARCHITECTURE.md` (EN), `CHANGELOG.md` (TR), `ROADMAP.md` (TR) dokümantasyon dosyaları oluşturuldu.
- `pyproject.toml` eklenerek `black` ve `ruff` biçimlendirme/lint yapılandırması projeye dahil edildi.

### Değiştirildi
- `udp_listener.py`: Timeout, drain-keep-latest tampon döngüsü, veri ayrıştırma (hız/RPM dönüşümleri, clamp'ler) satır içi teknik açıklamalarla belgelendi.
- `ROADMAP.md`: Eski alfa fazları sadeleştirilerek 5 ana hedef başlığı altında toplandı.

---

## [Erken Geliştirme Dönemi (2026-02 – 2026-06)]

`development_log.md` içindeki ilk prototip ve alfa geliştirme sürecinin özeti:

- **Telemetri & UDP Altyapısı (`core/udp_listener.py`):** 264 baytlık DiRT Rally 2.0 UDP paketlerini dinleyen `socket` yapısı ve `struct.unpack` ayrıştırıcısı kuruldu. Gecikmeyi önleyen buffer drain mekanizması geliştirildi.
- **Dijital Gösterge (`dashboards/digital_dash.py`):** Koyu temalı modern arayüz, devir oranına göre renk değiştiren dinamik RPM barı, tekerlek/araç hız farkına dayalı çekiş kaybı (SLIP) uyarısı, gaz/fren pedal göstergeleri ve kompakt WRC/F1 düzeni oluşturuldu.
- **Analog Gösterge (`dashboards/analog_dash.py`):** Trigonometrik iğne mekanizması, lineer enterpolasyon ile yumuşatma, 9000 RPM sabit kadran ve araca göre dinamik redline sınırı geliştirildi.
- **Raspberry Pi Vites Işıkları (`core/led_controller.py`):** `gpiozero` ile devir oranına göre Yeşil → Mavi → Kırmızı LED vites ışığı kontrolü eklendi.
- **Windows Saydam Overlay (`core/overlay_win.py`):** Windows Win32 API (`ctypes`) entegrasyonu ile çerçevesiz, yarı saydam (`alpha` / `chroma`), tıklama geçiren (`WS_EX_TRANSPARENT`) ve her zaman üstte (`HWND_TOPMOST`) oyun üzeri katman modu sağlandı.
- **Yapılandırma & Temalandırma (`config.py` & `settings.py`):** Sistem ayarları ile görsel temalar ayrıştırıldı; `TARGET_WIDTH` ile orantılı ölçeklendirme ve gösterge stili seçimi (`digital` / `analog`) merkezi hale getirildi.
