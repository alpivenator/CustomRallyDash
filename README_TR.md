# CustomRallyDash — DiRT Rally 2.0 Telemetri Göstergesi

[English](README.md) | **Türkçe**

**CustomRallyDash**, **DiRT Rally 2.0** için geliştirilmiş gerçek zamanlı bir telemetri gösterge panelidir (HUD). Oyunun fizik motorundan gelen 60 Hz UDP (`Extradata=3`) paketlerini çözümler ve son derece düşük gecikmeli görsel enstrümantasyon sunar. Kompakt dijital HUD, dairesel analog devir saati, Windows için çerçevesiz ve tıklama geçirgen kaplama modu ile Raspberry Pi GPIO ile yakılan vites ışıklarını destekler.

![DiRT Rally 2.0 Telemetri Kaplama Önizlemesi](images/digital_hood_chroma.webp)

---

## Özellikler

- **Gösterge Düzenleri**: Modern yatay dijital çubuk HUD ve dinamik dairesel analog kadran.
- **Windows Pencere Kaplaması (Overlay)**: Oyun sırasında daima üstte kalan, `alpha` (yarı saydam) ve `chroma` (renk anahtarlı tam şeffaf) kompozitleme modlarına sahip tıklama geçirgen pencere.
- **Motor Sporları Temaları**: Seçilmiş renk paletlerini içeren etkileşimli tema seçici (`Modern Dark`, `Subaru WRC`, `GT3 Racing`, `Night Neon`, `Retro Amber`).
- **Simüle Telemetri Yayıncısı (Mock Broadcaster)**: Oyunu açmadan çevrimdışı test ve görsel ayar yapabilmeniz için WRC hızlanma, sıralı vites geçişleri ve sol ayak frenajını taklit eden 60 Hz bağımsız sentetik paket üreteci.
- **Donanımsal Vites Işıkları**: Raspberry Pi GPIO (`gpiozero`) üzerinden fiziksel LED entegrasyonu.
- **Doğrudan Python Yapılandırması**: Harici dosya ayrıştırıcı yükü olmaksızın doğrudan standart Python dosyaları (`config.py` çalışma zamanı ve sistem için, `settings.py` arayüz ve stil için) üzerinden yapılandırma.

---

## Gereksinimler

- **Python**: `3.11.x`, `3.12.x` veya `3.13.x` (Python 3.14+ şu an için desteklenmemektedir)
- **Bağımlılıklar**: `pygame==2.6.1`, `gpiozero==2.0.1` (isteğe bağlı, yalnızca Raspberry Pi için)

---

## Hızlı Başlangıç

### Windows

Depo kök dizininde yer alan hazır toplu işlem (.bat) betiklerini kullanabilirsiniz:

| Betik | Amaç | Açıklama |
| :--- | :--- | :--- |
| `install.bat` | **İlk Kurulum** | `.venv` sanal ortamını oluşturur, bağımlılıkları yükler ve kurulum sihirbazını başlatır. |
| `run_dash.bat` | **Göstergeyi Başlat** | Telemetri gösterge panelini çalıştırır. |
| `select_theme.bat` | **Tema Seçici** | Motor sporları renk paletlerini uygulamak için etkileşimli terminal arayüzü. |
| `run_mock.bat` | **Çevrimdışı Önizleme** | Test amaçlı 60 Hz simüle telemetri yayını yapar. |
| `check_telemetry.bat` | **Tanılama** | Oyundan UDP paketlerinin gelip gelmediğini dinler ve bağlantıyı doğrular. |

> **ZIP olarak indirenler için not**: Projeyi Windows'a `.zip` olarak indirdiyseniz, arşiv dosyasına sağ tıklayıp *Özellikler → "Engellemeyi Kaldır" (Unblock) → Uygula* adımlarını uyguladıktan sonra çıkartın.

### Linux ve Komut Satırı

```sh
# 1. Ortam Kurulumu
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Etkileşimli Kurulum Sihirbazı (config.py ve oyun XML dosyasını yapılandırır)
python tools/setup_wizard.py

# 3. Göstergeyi Başlat
python main.py

# İsteğe bağlı: Göstergeyi simüle (mock) telemetri ile aç
python main.py --mock

# İsteğe bağlı: Görsel temayı değiştir
python tools/theme_selector.py
```

---

## Oyun UDP ve Ekran Yapılandırması

DiRT Rally 2.0'ın UDP telemetrisi yayını yapabilmesi için `hardware_settings_config.xml` dosyasında yapılandırılması gerekir:

```text
Belgeler\My Games\DiRT Rally 2.0\hardwaresettings\hardware_settings_config.xml
```

`<motion_platform>` bölümünün aşağıdaki girdiyi içerdiğinden emin olun:

```xml
<udp enabled="true" extradata="3" ip="127.0.0.1" port="20777" delay="1" />
```

*Çoklu makine kurulumlarında (gösterge paneli ayrı bir bilgisayarda veya Raspberry Pi'de çalışıyorsa), `ip` değerini göstergenin çalıştığı cihazın yerel ağ (LAN) IPv4 adresi olarak ayarlayın.*

> **Önemli (Windows Kaplama Modu)**: Tıklama geçirgen kaplama penceresinin oyun sırasında daima en üstte kalabilmesi için DiRT Rally 2.0 görüntü ayarlarını **Pencereli (Windowed)** veya **Çerçevesiz Pencereli (Borderless Windowed)** moda getirin.

---

## Mimari ve Yapılandırma

- `config.py` — Sistem ayarları: Ağ arayüzü (`LISTEN_IP`, `LISTEN_PORT`), gösterge stili (`DASH_STYLE`), kaplama anahtarı (`ENABLE_OVERLAY`) ve donanım bayrakları.
- `settings.py` — Görsel ve kaplama ayarları: Pencere boyutları, ölçekleme (`TARGET_SCALE`), kaplama konumu ve saydamlık modu (`OVERLAY_MODE`, `OVERLAY_POSITION`, `OVERLAY_CHROMA_KEY`), renk paletleri ve yazı tipi boyutları.
- `core/` — Telemetri paket ayrıştırıcısı (`udp_listener.py`), Windows saydam kaplama kancaları (`overlay_win.py`) ve GPIO LED sürücüsü (`led_controller.py`).
- `dashboards/` — Pygame çizim modülleri (`digital_dash.py`, `analog_dash.py`) ve tema tanımları (`themes.py`).
- `tools/` — İlk çalıştırma sihirbazı (`setup_wizard.py`), paket tanılama aracı (`telemetry_check.py`), simüle telemetri üreteci (`mock_telemetry.py`) ve tema komut satırı aracı (`theme_selector.py`).

Ayrıntılı yapılandırma seçenekleri ve güvenlik yönergeleri için [docs/CONFIGURATION_TR.md](docs/CONFIGURATION_TR.md) belgesine göz atın.

---

## Dokümantasyon

- [Mimari ve Veri Akışı](docs/ARCHITECTURE_TR.md) ([English](docs/ARCHITECTURE.md))
- [Yapılandırma Kılavuzu](docs/CONFIGURATION_TR.md) ([English](docs/CONFIGURATION.md))
- [Sürüm Geçmişi (Changelog)](docs/CHANGELOG_TR.md) ([English](docs/CHANGELOG.md))
- [Yol Haritası (Roadmap)](docs/ROADMAP_TR.md) ([English](docs/ROADMAP.md))

---

## Lisans

Bu proje **MIT** lisansı ile lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakabilirsiniz.
