# Yapılandırma Kılavuzu — CustomRallyDash

[English](CONFIGURATION.md) | **Türkçe**

CustomRallyDash, yapılandırma için ek dosya ayrıştırıcılarına gerek kalmadan doğrudan standart Python dosyalarını kullanır. Yapılan değişiklikler uygulamanın bir sonraki başlatılışında geçerli olur (çalışma zamanında dinamik yeniden yükleme / hot-reload yoktur).

- **`config.py`** — Çalışma zamanı ve donanım ayarları (ağ arayüzü, gösterge stili, Windows kaplama anahtarı, Raspberry Pi LED'leri).
- **`settings.py`** — Görsel biçimlendirme ayarları (çözünürlük, ölçekleme, renkler, yazı tipleri, kaplama konumu ve saydamlık modu).

> **İpucu**: Kodları genellikle elle düzenlemeniz gerekmez. İlk kurulumu `install.bat` (veya `python tools/setup_wizard.py`) sihirbazıyla yapabilir, görsel renk temalarını ise `select_theme.bat` (veya `python tools/theme_selector.py`) aracıyla kolayca değiştirebilirsiniz.

---

## Hızlı Yapılandırma (En Sık Kullanılan Ayarlar)

Çoğu kullanıcı için yalnızca aşağıdaki temel ayarlar yeterlidir:

| Amaç | Dosya | Değişken | Varsayılan / Önerilen |
| :--- | :--- | :--- | :--- |
| **Gösterge stilini değiştirme** | `config.py` | `DASH_STYLE` | `"digital"` (yatay çubuklu HUD) veya `"analog"` (dairesel kadran) |
| **Gösterge boyutunu ölçekleme** | `settings.py` | `TARGET_SCALE` | `None` (özgün boyut), `1.25` (+%25 büyütme), `0.8` (-%20 küçültme) |
| **Windows kaplamasını açma/kapatma** | `config.py` | `ENABLE_OVERLAY` | `True` (Windows üzerinde saydam ve tıklama geçirgen kaplama modu) |
| **Kaplama konumunu ayarlama** | `settings.py` | `OVERLAY_POSITION` | `"bottom-right"` (sağ alt), `"bottom-center"` (alt orta), `"bottom-left"` (sol alt) |
| **Renk temasını değiştirme** | `settings.py` | *(Otomatik)* | Hazır motor sporları temalarını uygulamak için `select_theme.bat` çalıştırın |
| **Telemetri IP adresi** | `config.py` | `LISTEN_IP` | `"127.0.0.1"` (aynı bilgisayar) veya gösterge LAN IP'si (çift bilgisayar) |

---

## Oyun Kurulumu (DiRT Rally 2.0 Telemetri Ayarı)

DiRT Rally 2.0'ın 60 Hz UDP telemetrisi göndermesini sağlamak için oyun yapılandırma dosyasını düzenleyin:

```text
Belgeler\My Games\DiRT Rally 2.0\hardwaresettings\hardware_settings_config.xml
```

`<motion_platform>` bölümünü bulun ve `<udp>` etiketini aşağıdaki şekilde güncelleyin veya doğrulayın:

```xml
<udp enabled="true" extradata="3" ip="127.0.0.1" port="20777" delay="1" />
```

- **Tek Bilgisayar**: `ip="127.0.0.1"` olarak bırakın.
- **Çift Bilgisayar / Raspberry Pi Kurulumu**: `ip` değerini CustomRallyDash'in çalıştığı bilgisayarın yerel ağ IPv4 adresiyle değiştirin (ör. `192.168.1.50`).

> **Pencere Üstü Kaplama (Overlay) Kullananlar İçin Önemli**: Oyun içi tıklama geçirgen kaplamanın (click-through overlay) her zaman oyunun üzerinde kalabilmesi için DiRT Rally 2.0 görüntü ayarlarını **Çerçevesiz Pencereli (Borderless Windowed)** veya **Pencereli (Windowed)** moda getirin.

---

## Test ve Doğrulama Araçları

Aşağıdaki komut dosyalarını kök dizinden doğrudan çalıştırabilirsiniz:

- **Bağlantı Testi**: `check_telemetry.bat` (veya `python tools/telemetry_check.py`) çalıştırın. Oyundan geçerli 264 baytlık UDP telemetri paketlerinin gelip gelmediğini doğrular.
- **Çevrimdışı Önizleme**: `python main.py --mock` komutunu çalıştırın (veya `run_mock.bat` ile `run_dash.bat` ikilisini açın). Oyunu açmaya gerek kalmadan gerçekçi WRC hızlanma ve fren verileriyle göstergeyi simüle eder.
- **Tema Seçici**: `select_theme.bat` (veya `python tools/theme_selector.py`) çalıştırın. *Subaru WRC*, *GT3 Racing*, *Night Neon* gibi hazır renk profillerini `settings.py` dosyasına otomatik yazar.

---

## Ayrıntılı Sistem Ayarları (`config.py`)

| Değişken | Tür | Varsayılan | Açıklama |
| :--- | :--- | :--- | :--- |
| `DASH_STYLE` | `str` | `"digital"` | Gösterge çeşidi: `"digital"` (600×200 px kompakt yatay HUD) veya `"analog"` (600×350 px dairesel devir saati). |
| `LISTEN_IP` | `str` | `"127.0.0.1"` | UDP soketinin bağlanacağı ağ arayüzü. Yerel oyun için `"127.0.0.1"`, uzaktaki oyun bilgisayarı için LAN IP'si veya `"0.0.0.0"`. |
| `LISTEN_PORT` | `int` | `20777` | Oyun XML dosyasında belirtilen portla eşleşen UDP dinleme portu. |
| `ENABLE_OVERLAY` | `bool` | `True` | Çerçevesiz, saydam ve tıklama geçirgen kaplama penceresini (click-through overlay) etkinleştirir (Yalnızca Windows; Linux'ta göz ardı edilir). |
| `ENABLE_LEDS` | `bool` | `False` | Raspberry Pi GPIO üzerinden fiziksel vites değiştirme LED ışıklarını (shift lights) etkinleştirir (`gpiozero` gerektirir). |

---

## Ayrıntılı Görsel ve Kaplama Ayarları (`settings.py`)

### Ekran Çözünürlüğü ve Kaplama Konumu

| Değişken | Varsayılan | Açıklama |
| :--- | :--- | :--- |
| `TARGET_SCALE` | `None` | Orantılı ölçekleme çarpanı (ör. `1.5` değeri dijital HUD'ı 600×200'den 900×300 piksele çıkarır; yazı tipleri otomatik ölçeklenir). `None` orijinal boyutu korur. |
| `DIGITAL_WIDTH` / `HEIGHT` | `600` / `200` | Dijital göstergenin varsayılan piksel çözünürlüğü. |
| `ANALOG_WIDTH` / `HEIGHT` | `600` / `350` | Analog kadrannın varsayılan piksel çözünürlüğü. |
| `OVERLAY_POSITION` | `"bottom-right"` | Windows üzerindeki ekran konumu: `"bottom-right"` (sağ alt), `"bottom-center"` (alt orta), `"bottom-left"` (sol alt). |
| `OVERLAY_MARGIN` | `20` | Ekran kenarlarından piksel cinsinden bırakılacak boşluk mesafesi. |
| `OVERLAY_MODE` | `"chroma"` | Pencere saydamlık modu: `"chroma"` (arka plan rengi tamamen şeffaflaştırılır) veya `"alpha"` (yarı saydam pencere paneli). |
| `OVERLAY_ALPHA` | `220` | `OVERLAY_MODE = "alpha"` iken pencere opaklığı (`0` = tamamen şeffaf/görünmez, `255` = tamamen mat). |
| `OVERLAY_CHROMA_KEY` | `COLOR_BG` | `"chroma"` modunda şeffaf yapılacak renk anahtarı. Varsayılan olarak dinamik biçimde `COLOR_BG` değerini işaret eder. |

### Renk Paleti ve Devir Kesici Eşiği

| Değişken | Varsayılan | Açıklama |
| :--- | :--- | :--- |
| `RPM_WARNING_THRESHOLD` | `0.90` | Devir kesici uyarı oranını belirler (0.0–1.0). Maksimum devrin %90'ına ulaşıldığında gösterge kırmızıya döner/yanıp söner. |
| `COLOR_BG` | `(25, 25, 30)` | Gösterge arka plan rengi (RGB). |
| `COLOR_RPM_NORMAL` | `(0, 150, 255)` | Devir kesici eşiğinin altındaki normal devir çubuğu / ibre rengi. |
| `COLOR_RPM_WARNING` | `(255, 40, 40)` | Devir kesiciye yaklaşıldığında veya aşıldığında yanan uyarı rengi. |
| `COLOR_THROTTLE` | `(40, 220, 100)` | Gaz pedalı gösterge çubuğu rengi. |
| `COLOR_BRAKE` | `(255, 60, 60)` | Fren pedalı gösterge çubuğu rengi. |
| `COLOR_TEXT_MAIN` | `(240, 240, 240)` | Birincil yüksek kontrastlı metin rengi. |
| `COLOR_TEXT_DIM` | `(180, 180, 180)` | İkincil / soluk etiket metin rengi. |
| `COLOR_TEXT_OUTLINE` | `(0, 0, 0)` | Metinlerin okunabilirliğini artıran gölge / dış çizgi rengi. |
| `COLOR_FRAME` | `(80, 80, 90)` | Çerçeveler, ayırıcı çizgiler ve kadran halkası rengi. |
| `COLOR_REDLINE` | `(255, 65, 105, 110)` | Analog kadrandaki devir kesici bölgesi işareti (4. değer alfa saydamlığıdır). |

### Tipografi (Piksel Cinsinden Temel Yazı Boyutları)

Yazı tipi boyutları `TARGET_SCALE` tanımlandığında otomatik olarak aynı oranda çarpılır:

| Değişken | Varsayılan | Kullanım Alanı |
| :--- | :--- | :--- |
| `FONT_HUGE_SIZE` | `82` | Vites gösterge değeri |
| `FONT_LARGE_SIZE` | `50` | Hız gösterge değeri (km/sa) |
| `FONT_MEDIUM_SIZE` | `22` | Dijital HUD'daki sayısal devir (RPM) metni |
| `FONT_SMALL_SIZE` | `18` | Yardımcı telemetri etiketleri (KM/H, RPM, Gear) |
| `FONT_TINY_SIZE` | `14` | Kadran rakamları ve pedal etiketleri (THR / BRK) |

---

## Güvenlik ve Ağ Notları

Oyun telemetri akışı, yerel ağ üzerinde şifrelenmemiş ve kimlik doğrulamasız UDP yayını olarak iletilir. Uygulamayı yalnızca güvendiğiniz yerel ağlarda çalıştırın. Bilgisayarınızda birden çok ağ bağdaştırıcısı varsa, `LISTEN_IP` ayarına `"0.0.0.0"` yerine ilgili ağ kartının yerel IPv4 adresini yazarak dinlemeyi sınırlandırabilirsiniz.
