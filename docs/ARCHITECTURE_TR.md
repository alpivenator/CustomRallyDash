# Mimari: CustomRallyDash

[English](ARCHITECTURE.md) | **Türkçe**

CustomRallyDash, DiRT Rally 2.0 için geliştirilmiş gerçek zamanlı bir telemetri göstergesidir. Oyun 60 Hz frekansında `Extradata=3` biçiminde 264 baytlık ham UDP paketleri gönderir. Uygulama bu paketleri yakalayıp ilgili alanları ayrıştırır ve veriyi kompakt dijital HUD ya da dairesel analog kadran olarak ekrana çizer. Windows'ta pencereyi oyunun üzerinde kalan tıklama geçirgen bir overlay'e dönüştürebilir, Raspberry Pi'de ise motor devrini GPIO vites ışıklarına aktarabilirsiniz.

## Dizin yapısı ve dosya görevleri

```text
CustomRallyDash/
├── .github/
│   ├── workflows/
│   │   └── ci.yml            # GitHub Actions CI (ruff, pytest, pip-audit, bash -n install.sh)
│   └── ISSUE_TEMPLATE/       # Hata bildirimi ve özellik talebi şablonları
├── .gitattributes            # Git satır sonu kuralları (.bat için CRLF, .sh için LF)
├── core/
│   ├── __init__.py           # Telemetri ve platform yardımcıları için paket dışa aktarımları
│   ├── udp_listener.py       # UDP soket dinleyicisi ve Extradata=3 paket çözücüsü
│   ├── overlay_win.py        # Windows Win32 ctypes overlay yardımcıları
│   └── led_controller.py     # Raspberry Pi GPIO vites ışığı sürücüsü (gpiozero)
├── dashboards/
│   ├── __init__.py           # Gösterge modülleri için paket dışa aktarımları
│   ├── digital_dash.py       # Kompakt dijital gösterge (600x200 px)
│   ├── analog_dash.py        # Analog kadran göstergesi (600x350 px)
│   └── themes.py             # Motor sporları ve simülasyon renk temaları
├── docs/                     # Mimari, yapılandırma, yol haritası ve sürüm geçmişi
├── images/                   # WebP önizleme ekran görüntüleri
├── tests/                    # Birim testleri (pytest)
├── tools/
│   ├── __init__.py           # Kurulum ve tanılama araçları için paket dışa aktarımları
│   ├── cli_ui.py             # Ortak Rich panelleri/tabloları ve ok tuşlu CLI yardımcıları
│   ├── setup_wizard.py       # İki dilli (EN/TR) ilk kurulum CLI sihirbazı
│   ├── telemetry_check.py    # UDP bağlantı doğrulama aracı
│   ├── mock_telemetry.py     # 60 Hz sentetik UDP paket üreteci
│   └── theme_selector.py     # Etkileşimli CLI tema seçici
├── config.py                 # Sistem ve donanım yapılandırması
├── settings.py               # Görsel düzen ve stil yapılandırması
├── main.py                   # Ana giriş noktası (--mock destekler)
├── pyproject.toml            # Proje meta verileri, Ruff/Black ve pytest ayarları
├── requirements.txt          # Temel Python bağımlılıkları (pygame, rich, questionary)
├── requirements-pi.txt       # İsteğe bağlı Raspberry Pi bağımlılığı (gpiozero)
├── LICENSE                   # MIT lisansı
├── AGENTS.md                 # Katkı sağlayanlar ve kodlama ajanları için proje kılavuzu
├── README.md                 # Proje genel bakışı ve hızlı başlangıç (İngilizce)
├── README_TR.md              # Proje genel bakışı ve hızlı başlangıç (Türkçe)
├── install.bat               # Windows ortam kurulumu ve sihirbaz başlatıcısı
├── install.sh                # Linux/Raspberry Pi ortam kurulumu ve sihirbaz başlatıcısı
├── run_dash.bat              # Windows gösterge başlatıcısı
├── run_mock.bat              # Windows mock telemetri başlatıcısı
├── select_theme.bat          # Windows tema seçici başlatıcısı
└── check_telemetry.bat       # Windows telemetri kontrol başlatıcısı
```

| Modül / dosya | Sorumluluk |
| :--- | :--- |
| `main.py` | Ana giriş noktası. `config.DASH_STYLE` değerini okur, gerekirse `--mock` iş parçacığını açar ve seçili göstergeyi başlatır. |
| `config.py` | Görsel olmayan ayarlar: dinleme IP/portu, LED anahtarı, overlay anahtarı ve gösterge stili. Kullanıcı elle veya `setup_wizard.py` ile düzenleyebilir. |
| `settings.py` | Görsel ayarlar: taban çözünürlük, ölçek çarpanı, renkler, yazı boyutları ve overlay konumu. Kullanıcı elle veya `theme_selector.py` ile düzenleyebilir. |
| `core/udp_listener.py` | 264 baytlık UDP paketlerini dinler, `struct.unpack("66f", ...)` ile çözer ve `TelemetryData` döner. |
| `core/overlay_win.py` | Çerçevesiz, şeffaf ve tıklama geçirgen pencere için Win32 (`ctypes`) çağrılarını yönetir. |
| `core/led_controller.py` | `config.ENABLE_LEDS` `True` olduğunda `gpiozero` üzerinden Raspberry Pi GPIO vites ışıklarını sürer. |
| `dashboards/digital_dash.py` | Dijital HUD (600x200 px): devir çubuğu, vites, hız ve pedal çubukları. |
| `dashboards/analog_dash.py` | Analog kadran (600x350 px): yumuşatılmış ibre, kadran çizgileri, dinamik redline bölgesi ve merkezi vites göstergesi. |
| `dashboards/themes.py` | Beş hazır renk paleti (`modern_dark`, `subaru_classic`, `gt3_racing`, `night_neon`, `retro_amber`). |
| `tools/cli_ui.py` | CLI araçları için ortak terminal arayüzü (`rich` panel/tablo/spinner ve metin geri dönüşlü `questionary` ok tuşu menüsü). |
| `tools/setup_wizard.py` | Türkçe ve İngilizce destekli ilk kurulum sihirbazı; `config.py` ve oyun XML'ini yedekleyip günceller. |
| `tools/telemetry_check.py` | Geçerli bir 264 baytlık UDP paketi için en fazla 5 saniye bekleyen bağımsız CLI kontrol aracı. |
| `tools/mock_telemetry.py` | Oyun açık değilken test yapabilmek için 60 Hz'de sentetik 264 baytlık UDP paketleri gönderir. |
| `tools/theme_selector.py` | `settings.py` dosyasını yedekleyip `dashboards/themes.py` içinden seçilen temayı uygulayan etkileşimli CLI aracı. |
| `install.bat` | `.venv` ortamını kurar, `requirements.txt` bağımlılıklarını yükler ve `tools/setup_wizard.py` sihirbazını açar. |
| `install.sh` | Linux/Raspberry Pi üzerinde `.venv` ortamını kurar, `requirements.txt` bağımlılıklarını yükler (`--pi` / `--dev` seçenekli) ve `tools/setup_wizard.py` sihirbazını açar. |
| `run_dash.bat` | `.venv` içinde `main.py` dosyasını çalıştırır. |
| `run_mock.bat` | `.venv` içinde `tools/mock_telemetry.py` dosyasını çalıştırır. |
| `select_theme.bat` | `.venv` içinde `tools/theme_selector.py` dosyasını çalıştırır. |
| `check_telemetry.bat` | `.venv` içinde `tools/telemetry_check.py` dosyasını çalıştırır. |

## Çalışma zamanı akışı

```text
main.py
  │
  ├─ config.DASH_STYLE değerini oku  ("digital" | "analog")
  │
  ├─ seçili göstergeyi içe aktar ──► dashboards.digital_dash.run()
  │                              ──► dashboards.analog_dash.run()
  │
  └─ run():
       │
       ├─ pygame ekranını başlat
       ├─ (Windows) core.overlay_win.apply_overlay()  <- çerçevesiz, katmanlı
       ├─ core.UDPListener(config.LISTEN_IP, config.LISTEN_PORT)
       │
       └─ 60 FPS ana döngü:
            │
            ├─ listener.receive()          -> TelemetryData
            ├─ devir çubuğu/ibresi, hız, vites ve pedal çubuklarını çiz
            ├─ core.led_controller.update_leds(rpm_ratio)  (etkinse)
            └─ pygame.display.flip()
```

Windows'ta `install.bat`, Linux ve Raspberry Pi'de ise `install.sh` Python 3.11, 3.12 veya 3.13 ile sanal ortam oluşturup bağımlılıkları kurar ve `tools/setup_wizard.py` sihirbazını başlatır. Sihirbaz, donanım adımını işletim sistemine göre belirler: Windows'ta overlay (`ENABLE_OVERLAY`) ayarını, diğer sistemlerde ise `config.py` içinde tanımlıysa Raspberry Pi GPIO vites ışıklarını (`ENABLE_LEDS`) sorar. Yeni değerleri yazmadan önce `config.py`'nin zaman damgalı yedeğini alır ve mevcut yapılandırma arayüzünü bozmadan yalnızca seçili alanları günceller. DiRT Rally 2.0'ın `hardware_settings_config.xml` dosyası bulunduğunda onu da yedekleyip `<udp>` satırını günceller.

## Veri akışı

```text
DiRT Rally 2.0  (60 Hz UDP yayını, Extradata=3)
        │
        ▼
core.udp_listener.py
   - 264 baytlık paket -> struct.unpack("66f", paket)
   - m/s -> km/sa dönüşümü, vites eşleme, pedal değerlerini [0, 1] aralığına kırpma
        │
        ▼
TelemetryData (namedtuple)
   wheel_speed_kmh : int    # dört tekerleğin hız ortalaması (km/sa)
   car_speed_kmh   : int    # aracın boyuna hızı (km/sa)
   rpm             : int    # motor devri (x10 çarpanı uygulanmış)
   max_rpm         : int    # devir kesici / redline (x10 çarpanı)
   gear_str        : str    # "N", "R" veya "1".."6"
   throttle        : float  # 0.0 .. 1.0 (kırpılmış)
   brake           : float  # 0.0 .. 1.0 (kırpılmış)
        │
        ├─► dashboards/digital_dash.py : devir çubuğu, hız, vites, pedal çubukları
        ├─► dashboards/analog_dash.py  : ibre, kadran çizgileri, dinamik redline
        └─► core/led_controller.py     : yeşil -> mavi -> kırmızı vites ışıkları
```

## Platform notları

- **Windows**: `config.py` içinde `ENABLE_OVERLAY = True` ise `core/overlay_win.py` pygame penceresini çerçevesiz (`WS_POPUP`), katmanlı (`WS_EX_LAYERED`), tıklama geçirgen (`WS_EX_TRANSPARENT`) ve daima en üstte (`HWND_TOPMOST`) tutar. `settings.py` iki saydamlık modu destekler:
  - `chroma` (varsayılan): `OVERLAY_CHROMA_KEY` rengini (varsayılan olarak `COLOR_BG` ile aynıdır) `LWA_COLORKEY` ile tamamen şeffaf yapar.
  - `alpha`: `OVERLAY_ALPHA` değerine (`0-255`) göre tüm pencereye `LWA_ALPHA` saydamlığı uygular.
- **Linux**: Overlay çağrıları yalnızca `sys.platform == "win32"` koşulunda çalışır. Linux'ta göstergeler standart bir pygame penceresinde açılır.
- **Raspberry Pi (isteğe bağlı)**: `ENABLE_LEDS = True` ayarlandığında `core/led_controller.py`, `rpm_ratio` değerine göre yeşil, mavi ve kırmızı GPIO LED'lerini yakar.
