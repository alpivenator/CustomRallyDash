# Mimari — CustomRallyDash

[English](ARCHITECTURE.md) | **Türkçe**

**CustomRallyDash**, **DiRT Rally 2.0** için özel olarak geliştirilmiş gerçek zamanlı bir telemetri gösterge paneli ve baş üstü göstergesidir (HUD). Oyun, ham 264 baytlık UDP paketlerini **Extradata=3** formatında 60 Hz frekansında yayınlar. Bu proje gelen paketleri yakalar, ilgili alanları çözümler ve sonucu kompakt bir **dijital gösterge** veya **analog kadran** olarak görselleştirir. İsteğe bağlı olarak Windows üzerinde tıklama geçirgen kaplama (click-through overlay) olarak konumlandırılabilir ve Raspberry Pi üzerindeki fiziksel vites ışıklarına (shift lights) yansıtılabilir.

## Dizin Yapısı ve Dosya Görevleri

```
ralli-codex/
├── .github/
│   ├── workflows/
│   │   └── ci.yml            # Otomatik GitHub Actions CI (ruff + pytest)
│   └── ISSUE_TEMPLATE/       # GitHub hata bildirimi ve özellik talebi şablonları
├── core/
│   ├── __init__.py           # Telemetri ve platform yardımcıları için paket dışa aktarımları
│   ├── udp_listener.py       # UDP soket dinleyicisi ve Extradata=3 paket çözücüsü
│   ├── overlay_win.py        # Windows Win32 ctypes kaplama (overlay) yardımcıları
│   └── led_controller.py     # Raspberry Pi GPIO vites ışığı sürücüsü (gpiozero)
├── dashboards/
│   ├── __init__.py           # Gösterge çalıştırıcıları için paket dışa aktarımları
│   ├── digital_dash.py       # Kompakt dijital gösterge (600×200 px)
│   ├── analog_dash.py        # Analog kadran göstergesi (600×350 px)
│   └── themes.py             # Motor sporları ve simülatör renk tema profilleri
├── tools/
│   ├── __init__.py           # Kurulum ve tanılama araçları paket dışa aktarımları
│   ├── setup_wizard.py       # İki dilli (TR/EN) ilk kurulum CLI sihirbazı
│   ├── telemetry_check.py    # UDP bağlantı tanılama aracı
│   ├── mock_telemetry.py     # 60 Hz sentetik UDP paket üreteci
│   └── theme_selector.py     # Bağımsız CLI tema seçici
├── docs/                     # Mimari, yapılandırma, yol haritası ve değişiklik belgeleri
│   ├── ARCHITECTURE.md       # Teknik tasarım ve mimari referansı (İngilizce)
│   ├── ARCHITECTURE_TR.md    # Teknik tasarım ve mimari referansı (Türkçe)
│   ├── CONFIGURATION.md      # Yapılandırma seçenekleri ve donanım kurulumu (İngilizce)
│   ├── CONFIGURATION_TR.md   # Yapılandırma seçenekleri ve donanım kurulumu (Türkçe)
│   ├── CHANGELOG.md          # Sürüm geçmişi (İngilizce)
│   ├── CHANGELOG_TR.md       # Sürüm geçmişi (Türkçe)
│   ├── ROADMAP.md            # Planlanan hedefler (İngilizce)
│   └── ROADMAP_TR.md         # Planlanan hedefler (Türkçe)
├── tests/                    # Birim testler (pytest)
├── README.md                 # Proje genel bakışı ve hızlı başlangıç (İngilizce)
├── README_TR.md              # Proje genel bakışı ve hızlı başlangıç (Türkçe)
├── main.py                   # Birleşik uygulama giriş noktası (--mock destekler)
├── config.py                 # Merkezi sistem ve donanım yapılandırması
├── settings.py               # Görsel düzen ve stil yapılandırması
├── install.bat               # Windows ortam kurulumu ve sihirbaz başlatıcı
├── run_dash.bat              # Windows gösterge başlatıcı
├── run_mock.bat              # Windows simüle telemetri başlatıcı
├── select_theme.bat          # Windows tema seçici başlatıcı
└── check_telemetry.bat       # Windows telemetri kontrol başlatıcı
```

| Modül / Dosya | Sorumluluk |
|---------------|------------|
| `main.py` | Birleşik giriş noktası. `config.DASH_STYLE` değerini okur ve ilgili göstergeyi başlatır. Otomatik önizleme için `--mock` parametresini destekler. |
| `config.py` | Görsel olmayan merkezi yapılandırma: dinleme IP/portu, LED etkinleştirme, kaplama (overlay) anahtarı, gösterge stili. Kullanıcı ve kurulum sihirbazı tarafından düzenlenir. |
| `settings.py` | Görsel yapılandırma: renkler, boyutlar, yazı tipleri, ekran konumları. Kullanıcı ve tema seçici tarafından düzenlenir. |
| `core/udp_listener.py` | 264 baytlık UDP paketlerini alır, `struct.unpack("66f", …)` ile ayrıştırır ve `TelemetryData` nesnesi döner. |
| `core/overlay_win.py` | Windows Win32 (`ctypes`) yardımcıları: çerçevesiz, saydam ve tıklama geçirgen (click-through) kaplama penceresi yönetimi. |
| `core/led_controller.py` | `gpiozero` kullanarak Raspberry Pi GPIO üzerindeki fiziksel vites ışıklarını sürer. `config.ENABLE_LEDS` ile açılır/kapanır. |
| `dashboards/digital_dash.py` | Kompakt dijital gösterge (600×200 px). Devir çubuğu, vites, hız ve pedal çubuklarını çizer. |
| `dashboards/analog_dash.py` | Analog kadran göstergesi (600×350 px). Trigonometrik ibre hareketi, kadran çizgileri, dinamik devir kesici bölgesi ve merkezi vites kutusu. |
| `dashboards/themes.py` | Hazır motor sporları renk paletleri (`modern_dark`, `subaru_classic`, `gt3_racing`, `night_neon`, `retro_amber`). |
| `tools/setup_wizard.py` | Türkçe ve İngilizce dil desteğine sahip ilk çalıştırma CLI kurulum sihirbazı. |
| `tools/telemetry_check.py` | Dış bağımlılık gerektirmeyen, geçerli telemetri paketlerini dinleyip doğrulayan CLI tanılama aracı. |
| `tools/mock_telemetry.py` | Oyunu açmaya gerek kalmadan canlı önizleme sunmak için 60 Hz frekansında sentetik 264 baytlık UDP paketleri üretir. |
| `tools/theme_selector.py` | Hazır renk paletlerini seçip `settings.py` dosyasına yazan etkileşimli CLI aracı. |
| `run_mock.bat` | Bağımsız simüle telemetri yayıncısı için Windows toplu işlem başlatıcısı. |
| `select_theme.bat` | Tema seçici için Windows toplu işlem başlatıcısı. |
| `check_telemetry.bat` | Telemetri bağlantı tanılaması için Windows toplu işlem başlatıcısı. |


## Çalışma Zamanı Akışı (Runtime Flow)

```
main.py
  │
  ├─ config.DASH_STYLE değerini oku  ("digital" | "analog")
  │
  ├─ seçilen göstergeyi içe aktar ──► dashboards.digital_dash.run()
  │                                ──► dashboards.analog_dash.run()
  │
  └─ run():
       │
       ├─ pygame ekranını başlat
       ├─ (Windows) core.overlay_win.apply_overlay()  ← çerçevesiz, katmanlı
       ├─ core.UDPListener(config.LISTEN_IP, config.LISTEN_PORT)
       │
       └─ 60 FPS ana döngü:
            │
            ├─ listener.receive()           → TelemetryData
            ├─ devir çubuğu/ibresi, hız, vites ve pedal barlarını çiz
            ├─ core.led_controller.update_leds(rpm_ratio)   (etkinse)
            └─ pygame.display.flip()
```

Windows platformunda `install.bat`, Python 3.11/3.12/3.13 sanal ortamını oluşturur ve `tools/setup_wizard.py` sihirbazını çalıştırır. Sihirbaz iki dilli bir arayüz (İngilizce / Türkçe) sunar; zaman damgalı bir yedek oluşturduktan sonra mevcut `config.py` dosyasını günceller. Böylece gösterge modülleri standart yapılandırma arayüzünü kesintisiz tüketmeye devam eder. Sihirbaz ayrıca tespit edildiğinde oyunun `hardwaresettings/hardware_settings_config.xml` dosyasını da yedekler ve günceller.

## Veri Akışı (Data Flow)

```
DiRT Rally 2.0  (60 Hz UDP yayını, Extradata=3)
        │
        ▼
core.udp_listener.py
   - 264 baytlık paket → struct.unpack("66f", paket)
   - m/s → km/sa dönüştür, vitesi çözümle, pedalları kırp (clamp)
        │
        ▼
TelemetryData (namedtuple)
   wheel_speed_kmh : int    # dört tekerleğin hız ortalaması (km/sa)
   car_speed_kmh   : int    # aracın boyuna eksendeki gerçek hızı (km/sa)
   rpm             : int    # motor devri (×10 çarpanı uygulanmış)
   max_rpm         : int    # devir kesici sınırı / redline (×10 çarpanı)
   gear_str        : str    # "N", "R" veya "1".."6"
   throttle        : float  # 0.0 .. 1.0 (kırpılmış gaz oranı)
   brake           : float  # 0.0 .. 1.0 (kırpılmış fren oranı)
        │
        ├─► dashboards/digital_dash.py : devir çubuğu, hız, vites, pedal barları
        ├─► dashboards/analog_dash.py  : ibre, kadran çizgileri, dinamik redline
        └─► core/led_controller.py     : yeşil → mavi → kırmızı vites ışıkları
```

## Platform Notları

- **Windows** — `config.py` içinde `ENABLE_OVERLAY = True` olduğunda göstergeler `core/overlay_win.py` aracılığıyla Win32 kaplama penceresine bağlanabilir. Pencere çerçevesiz (`WS_POPUP`), katmanlı (`WS_EX_LAYERED`), tıklama geçirgen (`WS_EX_TRANSPARENT`) ve daima en üsttedir (`HWND_TOPMOST`). `settings.py` içinde yapılandırılabilen iki saydamlık modu bulunur:
  - `chroma` (varsayılan) — tek bir anahtar renk (`OVERLAY_CHROMA_KEY`, dinamik olarak `COLOR_BG` değerini takip eder) `LWA_COLORKEY` ile tamamen saydamlaştırılır.
  - `alpha` — `LWA_ALPHA` ile piksel başına saydamlık uygulanır; opaklık `OVERLAY_ALPHA` (0–255) ile belirlenir.
- **Linux** — `overlay_win` modülü yalnızca `sys.platform.startswith("win")` durumunda içe aktarılır. Göstergeler standart bir pygame penceresinde çalışır.
- **Raspberry Pi (isteğe bağlı)** — `core/led_controller.py`, `rpm / max_rpm` oranına bağlı olarak GPIO vites ışıklarını sürer.
