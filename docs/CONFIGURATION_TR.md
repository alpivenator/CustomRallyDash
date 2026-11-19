# Yapılandırma kılavuzu: CustomRallyDash

[English](CONFIGURATION.md) | **Türkçe**

CustomRallyDash tüm ayarları doğrudan iki Python dosyasından okur. Değişiklikler bir sonraki başlatmada geçerli olur; çalışma sırasında otomatik yenileme (hot-reload) yoktur.

- `config.py`: Sistem, ağ, gösterge stili, Windows overlay ve Raspberry Pi LED ayarları.
- `settings.py`: Çözünürlük, ölçekleme, renk paleti, yazı tipi boyutları ve overlay yerleşim ayarları.

Bu dosyaları çoğu zaman elle düzenlemeniz gerekmez. İlk kurulum için Windows'ta `install.bat`, Linux ve Raspberry Pi'de `./install.sh` betiğini ya da doğrudan `python tools/setup_wizard.py` komutunu çalıştırabilirsiniz. Renk temasını değiştirmek için `select_theme.bat` veya `python tools/theme_selector.py` kullanabilirsiniz.

## Hızlı yapılandırma

Günlük kullanımda genellikle yalnızca aşağıdaki ayarlara ihtiyaç duyulur:

| Amaç | Dosya | Değişken | Varsayılan / seçenekler |
| :--- | :--- | :--- | :--- |
| Gösterge stilini değiştirme | `config.py` | `DASH_STYLE` | `"digital"` (yatay HUD) veya `"analog"` (dairesel kadran) |
| Boyutu ölçekleme | `settings.py` | `TARGET_SCALE` | `None` (özgün boyut), `1.25` (+%25), `0.8` (-%20) |
| Windows overlay'i açma/kapatma | `config.py` | `ENABLE_OVERLAY` | `True` (Windows'ta şeffaf ve tıklama geçirgen pencere) |
| Overlay konumunu değiştirme | `settings.py` | `OVERLAY_POSITION` | `"bottom-right"`, `"bottom-center"` veya `"bottom-left"` |
| Renk temasını seçme | `settings.py` | *(CLI aracı)* | Hazır paletleri uygulamak için `select_theme.bat` veya `python tools/theme_selector.py` çalıştırın |
| Telemetri IP adresi | `config.py` | `LISTEN_IP` | `"127.0.0.1"` (aynı PC) veya göstergenin LAN IP'si (ayrı cihaz) |

## Oyun kurulumu (DiRT Rally 2.0)

DiRT Rally 2.0'ın 60 Hz UDP telemetrisi göndermesi için oyun donanım yapılandırma dosyasını açın:

```text
Belgeler\My Games\DiRT Rally 2.0\hardwaresettings\hardware_settings_config.xml
```

`<motion_platform>` bölümünü bulup `<udp>` etiketini şu şekilde güncelleyin:

```xml
<udp enabled="true" extradata="3" ip="127.0.0.1" port="20777" delay="1" />
```

- Tek bilgisayar: `ip="127.0.0.1"` değerini koruyun.
- İkinci bilgisayar veya Raspberry Pi: `ip` alanına CustomRallyDash'in çalıştığı cihazın yerel ağ IPv4 adresini yazın (örneğin `192.168.1.50`).

Windows'ta overlay kullanacaksanız pencerenin oyun üzerinde kalabilmesi için DiRT Rally 2.0 görüntü ayarını **Pencereli (Windowed)** veya **Çerçevesiz Pencereli (Borderless Windowed)** yapın.

## Test ve doğrulama araçları

Proje kök dizininden şu araçları çalıştırabilirsiniz:

- Bağlantı testi: `check_telemetry.bat` (veya `python tools/telemetry_check.py`) oyundan 264 baytlık UDP paketlerinin gelip gelmediğini kontrol eder.
- Çevrimdışı önizleme: `python main.py --mock` komutunu kullanın veya `run_mock.bat` ile `run_dash.bat` betiklerini birlikte açın. Oyun açık olmasa da 60 Hz WRC hızlanma ve fren verisi üretilir.
- Tema seçici: `select_theme.bat` (veya `python tools/theme_selector.py`), `Subaru Classic WRC`, `GT3 Competition` ve `Night Stage Neon (Cyberpunk)` gibi hazır temaları `settings.py`'ye yazar.

## Sistem ayarları (`config.py`)

| Değişken | Tür | Varsayılan | Açıklama |
| :--- | :--- | :--- | :--- |
| `DASH_STYLE` | `str` | `"digital"` | Gösterge türü: `"digital"` (600x200 px yatay HUD) veya `"analog"` (600x350 px dairesel devir saati). |
| `LISTEN_IP` | `str` | `"127.0.0.1"` | UDP soketinin dinleyeceği arayüz. Yerel oyun için `"127.0.0.1"`, ayrı cihazlar için LAN IP'si veya `"0.0.0.0"`. |
| `LISTEN_PORT` | `int` | `20777` | UDP dinleme portu; oyun XML'indeki `port` değeriyle aynı olmalıdır. |
| `ENABLE_OVERLAY` | `bool` | `True` | Çerçevesiz, şeffaf ve tıklama geçirgen overlay penceresini açar (yalnızca Windows'ta çalışır, Linux'ta yok sayılır). |
| `ENABLE_LEDS` | `bool` | `False` | Raspberry Pi GPIO üzerinden fiziksel vites ışıklarını etkinleştirir (`gpiozero` gerektirir). |

## Görsel ve overlay ayarları (`settings.py`)

### Çözünürlük ve overlay konumu

| Değişken | Varsayılan | Açıklama |
| :--- | :--- | :--- |
| `TARGET_SCALE` | `None` | Orantılı ölçek çarpanı (örneğin `1.5`, dijital HUD'ı 600x200'den 900x300 piksele çıkarıp yazı boyutlarını da ölçekler). `None` taban boyutları korur. |
| `DIGITAL_WIDTH` / `HEIGHT` | `600` / `200` | Dijital HUD'ın piksel cinsinden taban çözünürlüğü. |
| `ANALOG_WIDTH` / `HEIGHT` | `600` / `350` | Analog kadranın piksel cinsinden taban çözünürlüğü. |
| `OVERLAY_POSITION` | `"bottom-right"` | Windows'ta pencere konumu: `"bottom-right"`, `"bottom-center"` veya `"bottom-left"`. |
| `OVERLAY_MARGIN` | `20` | Sol ve sağ konumlarda ekran kenarından piksel cinsinden boşluk. |
| `OVERLAY_MODE` | `"chroma"` | Saydamlık modu: `"chroma"` (arka plan rengini tamamen şeffaf yapar) veya `"alpha"` (yarı saydam pencere). |
| `OVERLAY_ALPHA` | `220` | `OVERLAY_MODE = "alpha"` iken pencere opaklığı (`0` görünmez, `255` tam mat). |
| `OVERLAY_CHROMA_KEY` | `COLOR_BG` | `"chroma"` modunda şeffaf yapılacak renk anahtarı. Varsayılan olarak `COLOR_BG` değerini izler. |

### Renk paleti ve redline eşiği

| Değişken | Varsayılan | Açıklama |
| :--- | :--- | :--- |
| `RPM_WARNING_THRESHOLD` | `0.90` | `max_rpm` değerine göre (`0.0-1.0`) uyarı rengine geçilen oran. Varsayılan olarak devrin %90'ında tetiklenir. |
| `COLOR_BG` | `(25, 25, 30)` | Arka plan rengi (RGB). |
| `COLOR_RPM_NORMAL` | `(0, 150, 255)` | Uyarı eşiği altındaki devir çubuğu ve ibre rengi. |
| `COLOR_RPM_WARNING` | `(255, 40, 40)` | Uyarı eşiğine ulaşıldığında veya aşıldığında kullanılan renk. |
| `COLOR_THROTTLE` | `(40, 220, 100)` | Gaz pedalı çubuğu rengi. |
| `COLOR_BRAKE` | `(255, 60, 60)` | Fren pedalı çubuğu rengi. |
| `COLOR_TEXT_MAIN` | `(240, 240, 240)` | Birincil metin rengi. |
| `COLOR_TEXT_DIM` | `(180, 180, 180)` | İkincil etiket rengi. |
| `COLOR_TEXT_OUTLINE` | `(0, 0, 0)` | Aydınlık etaplarda okunabilirliği artıran koyu metin dış çizgisi. |
| `COLOR_FRAME` | `(80, 80, 90)` | Çerçeveler, kadran halkası ve çubuk kenarlıkları. |
| `COLOR_REDLINE` | `(255, 65, 105, 110)` | Analog kadrandaki redline bölgesinin RGBA rengi (dördüncü değer alfa saydamlığıdır). |

### Yazı tipi boyutları

Piksel cinsinden verilen bu boyutlar `TARGET_SCALE` tanımlandığında otomatik olarak ölçeklenir:

| Değişken | Varsayılan | Kullanıldığı yer |
| :--- | :--- | :--- |
| `FONT_HUGE_SIZE` | `82` | Vites göstergesi |
| `FONT_LARGE_SIZE` | `50` | Hız değeri (`km/sa`) |
| `FONT_MEDIUM_SIZE` | `22` | Dijital HUD'daki sayısal devir (`RPM`) metni |
| `FONT_SMALL_SIZE` | `18` | Dijital HUD'da `SPEED` ve `GEAR`; analog kadranda `KM/H`, `THR` ve `BRK` etiketleri |
| `FONT_TINY_SIZE` | `14` | Dijital HUD'da `THR` ve `BRK` etiketleri; analog kadrandaki devir rakamları |

## Ağ ve güvenlik notları

DiRT Rally 2.0 telemetri akışı yerel ağda şifresiz ve kimlik doğrulamasız UDP yayını olarak gönderilir. Uygulamayı yalnızca güvendiğiniz ağlarda çalıştırın. Birden fazla ağ bağdaştırıcısı olan sistemlerde dinlemeyi kısıtlamak için `LISTEN_IP` alanına `"0.0.0.0"` yerine ilgili yerel IPv4 adresini yazabilirsiniz.
