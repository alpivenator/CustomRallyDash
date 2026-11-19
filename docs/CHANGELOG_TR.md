# Sürüm geçmişi

[English](CHANGELOG.md) | **Türkçe**

Projede yapılan değişiklikler ters kronolojik sırayla aşağıda listelenir. Planlanan hedefler için [ROADMAP_TR.md](ROADMAP_TR.md), mimari ayrıntılar için [ARCHITECTURE_TR.md](ARCHITECTURE_TR.md) dosyasına bakın.

## [v0.1.1] - 2026-09-09

### Değiştirildi
- `pyproject.toml`: Paket sürümü `0.1.1` olarak güncellendi.

### Düzeltildi
- `install.bat`: Windows Batch içindeki işaretli `errorlevel` davranışı nedeniyle Python 3.13 kurulu olmayan sistemlerde yaşanan sürüm algılama hatası giderildi ve `PATH` üzerindeki varsayılan `python` için yedek kontrol eklendi.

## [v0.1.0] - 2026-09-08

### Eklendi
- `.github/workflows/ci.yml`: CI hattına bağımlılık güvenlik açığı taraması için `pip-audit` adımı eklendi.
- `pyproject.toml`: Ruff güvenlik kuralları (`"S"`) `lint.select` listesine eklendi; testlerdeki `assert` ve XML ayrıştırma çağrıları için `per-file-ignores` (`tests/* = ["S101", "S314"]`) tanımlandı.

### Güvenlik
- `core/udp_listener.py` ve `tools/mock_telemetry.py`: Soket bağlama uyarı susturmaları `# noqa: S104` biçimine çevrildi.
- `tools/setup_wizard.py`: Yerel oyun XML okuma satırına `# noqa: S314` işareti eklendi.

### Not
- Python 3.14 uyumluluğu incelendi; PyPI üzerinde Pygame 2.6.1 için hazır wheel paketleri henüz bulunmadığından destek ertelendi. Çalışma zamanı kısıtı `>=3.11,<3.14` olarak kaldı.

## [2026-09-03]

### Eklendi
- `README_TR.md`: Dil geçiş bağlantılarıyla birlikte proje genel bakış ve hızlı başlangıç belgesinin Türkçe sürümü eklendi.
- `docs/CONFIGURATION_TR.md`: Yapılandırma kılavuzunun Türkçe sürümü eklendi.
- `docs/ARCHITECTURE_TR.md`: Mimari ve veri akışı belgesinin Türkçe sürümü eklendi.

### Değiştirildi
- `docs/CONFIGURATION.md`: Sık kullanılan ayarlar üstteki "Quick Configuration" tablosunda toplandı ve diğer ayarlar kapsamına göre gruplandı.
- `README.md` ve `docs/ARCHITECTURE.md`: Belge başlarına dil geçiş bağlantıları eklendi ve açıklamalar sadeleştirildi.
- `AGENTS.md`: Geliştirici yönergeleri İngilizce ve Türkçe belgelerin eşzamanlı güncellenmesini içerecek biçimde düzenlendi.
- Projenin adı **CustomRallyDash** olarak değiştirildi ve `pyproject.toml` meta verileri güncellendi (`name = "custom-rally-dash"`, `version = "0.1.0"`).
- `tools/setup_wizard.py` içindeki CLI başlıkları güncellendi.
- Proje lisansı `LICENSE`, `README.md` ve `pyproject.toml` dosyalarında GPL-3.0'dan MIT'ye çevrildi.

## [2026-09-02]

### Eklendi
- `README.md`: Başlık altına şeffaf dijital HUD'ın oyun içi önizleme görseli eklendi.
- `images/`: Ekran görüntüleri WebP formatına dönüştürülüp sıkıştırıldı; görsel dosya boyutu %90'ın üzerinde azaltıldı.

### Değiştirildi
- `pyproject.toml`, `README.md`, `install.bat`, `.github/workflows/ci.yml`, `docs/ARCHITECTURE.md`: Python desteği 3.11, 3.12 ve 3.13 (`>=3.11,<3.14`) sürümlerini kapsayacak şekilde genişletildi; varsayılan CI hedefi Python 3.13 yapıldı ve `install.bat` sırasıyla Python 3.13, 3.12 ve 3.11'i algılayacak biçimde güncellendi.

## [2026-09-01]

### Eklendi
- `dashboards/digital_dash.py` ve `dashboards/analog_dash.py`: Şeffaf overlay modunda aydınlık etaplar üzerinde okunabilirliği artırmak için tüm gösterge değerlerine ve etiketlere koyu dış çizgi (`draw_text_outlined`, `draw_text_outlined_center`) eklendi.
- `settings.py`: Metin dış çizgi rengi için `COLOR_TEXT_OUTLINE` (varsayılan `(0, 0, 0)`) ayarı eklendi.
- `README.md`: Windows overlay'inin görünür kalması için DiRT Rally 2.0'ın Pencereli veya Çerçevesiz Pencereli modda çalıştırılması gerektiği eklendi.
- `tests/test_themes_and_mock.py`: Overlay ayar yapısını ve dış çizgili metin çizimini doğrulayan birim testleri eklendi.

### Değiştirildi
- `config.py` ve `settings.py`: `config.py` içinde yalnızca `ENABLE_OVERLAY` anahtarı bırakıldı; görsel ve konum ayarları (`OVERLAY_MODE`, `OVERLAY_POSITION`, `OVERLAY_MARGIN`, `OVERLAY_ALPHA`, `OVERLAY_CHROMA_KEY`) `settings.py`'ye taşındı.
- `settings.py`: Varsayılan `OVERLAY_MODE` değeri `"chroma"`, `OVERLAY_POSITION` değeri `"bottom-right"` olarak ayarlandı ve `OVERLAY_CHROMA_KEY = COLOR_BG` eşitliğiyle aktif temaya bağlandı.
- `settings.py` ve `dashboards/themes.py`: Varsayılan `COLOR_REDLINE` rengi uyarı ibresinden ayrışması için `(255, 65, 105, 110)` tonuna çekildi.
- `core/overlay_win.py`: `apply_overlay` (`mode="chroma"`) ve `position_window` (`position="bottom-right"`) varsayılan argümanları güncellendi.
- `dashboards/analog_dash.py` ve `dashboards/digital_dash.py`: Devir uyarı eşiği okuması doğrudan `settings.RPM_WARNING_THRESHOLD` üzerinden yapılacak şekilde sadeleştirildi.
- `tools/setup_wizard.py`: Kurulum bitiş özetine (EN ve TR) çevrimdışı mock önizleme (`run_mock.bat` / `--mock`) ve tema seçici (`select_theme.bat`) adımları eklendi.
- `README.md`: Hızlı başlangıç tabloları ve komut satırı akışlarıyla sadeleştirildi.
- `config.py`: Varsayılan `DASH_STYLE` değeri `"digital"` olarak ayarlandı.
- `docs/CONFIGURATION.md`: `select_theme.bat` ve `run_mock.bat` açıklamalarıyla gösterge türü seçimi eklendi; overlay ayarları görsel ayarlar tablosuna taşındı.
- `docs/ARCHITECTURE.md`: Windows platform notları `settings.py` üzerindeki yeni yapıya göre güncellendi.

### Düzeltildi
- `dashboards/analog_dash.py`: `draw_redline_zone` işlevinde `pygame.draw.arc` yerine trigonometrik poligon dolgusu (`pygame.draw.polygon`) kullanılarak yay çizimindeki piksel boşlukları, moiré ve siyah nokta hataları giderildi.

## [2026-08-31]

### Eklendi
- `settings.py`: Uyarı rengine geçiş oranını yöneten `RPM_WARNING_THRESHOLD` (varsayılan `0.90`) ayarı eklendi.
- `tests/test_themes_and_mock.py`: `settings.RPM_WARNING_THRESHOLD` değerini doğrulayan birim testi eklendi.

### Değiştirildi
- `dashboards/analog_dash.py`: İbre uyarı rengi tetikleyicisi %100 redline yerine `max_rpm * RPM_WARNING_THRESHOLD` eşiğine çekildi.
- `dashboards/analog_dash.py`: Ortadaki vites dairesi vurgu halkasının çizgi kalınlığı artırıldı.
- `dashboards/digital_dash.py`: Devir çubuğunun uyarı rengine geçişi `settings.RPM_WARNING_THRESHOLD` ile eşitlendi.
- `README.md` ve `docs/CONFIGURATION.md`: Windows'ta indirilen ZIP arşivlerini çıkartmadan önce özelliklerden "Engellemeyi Kaldır" seçeneğinin işaretlenmesi gerektiği eklendi.

### Düzeltildi
- `pyproject.toml`: `tools`, `dashboards` ve `core` içe aktarımlarının yerel ve CI ortamlarında çözümlenmesi için `[tool.pytest.ini_options]` altına `pythonpath = ["."]` ve `testpaths = ["tests"]` eklendi.
- `.github/workflows/ci.yml`: Test komutu `python -m pytest` olarak sabitlendi.

## [2026-08-29]

### Değiştirildi
- `tools/mock_telemetry.py`: Mock döngüsü 15 saniyelik WRC hızlanma çevrimine göre ayarlandı; araç 9 saniyede 1'den 6. vitese (vites başına ~1,5 sn) çıkıp 205 km/sa hıza ulaşıyor.
- `tools/mock_telemetry.py`: Yakın oranlı sıralı şanzıman davranışı eklendi; 1. viteste 2500 RPM'den kalkıp üst vites geçişlerinde ~5800 RPM'e düşüyor.
- `tools/mock_telemetry.py`: 9-15 saniye arasındaki frenleme fazına kademeli vites düşürme (6->1), ~%50 gaz ara gazı darbesi (auto-blip) ve ~6800 RPM devir eşleme eklendi.

### Düzeltildi
- `tools/mock_telemetry.py`: Frenleme fazı 1. vitese ve durma/rölantiye kadar uzatıldı; 15 saniyelik döngü başa sararken oluşan ani vites sıçraması giderildi.

## [2026-08-28]

### Eklendi
- `dashboards/themes.py`: Beş hazır renk teması eklendi (`modern_dark`, `subaru_classic`, `gt3_racing`, `night_neon`, `retro_amber`).
- `tools/theme_selector.py` ve `select_theme.bat`: `settings.py` dosyasını yedekleyip güvenli biçimde tema değiştiren iki dilli (EN/TR) CLI aracı ve Windows başlatıcısı eklendi.
- `tools/mock_telemetry.py` ve `run_mock.bat`: Oyun açık olmadan hızlanma, vites geçişi, sert fren ve viraj çıkışı üreten 60 Hz Extradata=3 sentetik UDP yayını eklendi.
- `main.py`: Göstergeyi ve mock yayıncıyı birlikte açan `--mock` bayrağı eklendi (`python main.py --mock`).
- `.github/ISSUE_TEMPLATE/`: GitHub için `bug_report.yml` ve `feature_request.yml` şablonları eklendi.
- `tests/test_themes_and_mock.py`: Mock paket üretimi ve tema uygulama işlevleri için birim testleri eklendi.

### Değiştirildi
- `dashboards/analog_dash.py`: İbre, merkez pivot ve vites dairesinin çizim sırası güncellendi.
- `README.md`, `ARCHITECTURE.md` ve `ROADMAP.md`: Tema sistemi, mock önizleme araçları ve yeni paket yapısına göre güncellendi.

## [2026-08-20]

### Düzenleme
- `core/`: UDP dinleyicisi, Windows overlay ve GPIO LED sürücüsü `core/` paketine taşınıp (`udp_listener.py`, `overlay_win.py`, `led_controller.py`) `core/__init__.py` içinden dışa aktarıldı.
- `dashboards/`: Dijital ve analog paneller `dashboards/` paketine taşındı; `analogdash.py` adı `analog_dash.py` olarak değiştirildi.
- `tools/`: Kurulum sihirbazı ve bağlantı kontrolü `tools/` paketine taşındı; kök dizin yolu dinamik çözümlenecek şekilde ayarlandı.
- `main.py`: İçe aktarımlar `dashboards.digital_dash` ve `dashboards.analog_dash` yollarına güncellendi.
- `install.bat` ve `check_telemetry.bat`: Betik hedefleri `tools\setup_wizard.py` ve `tools\telemetry_check.py` olarak güncellendi.
- `tests/test_setup_wizard.py`: Birim testleri `tools.setup_wizard` ve `tools.telemetry_check` modüllerine göre güncellendi.
- `ARCHITECTURE.md`, `CONFIGURATION.md` ve `README.md`: Dosya yolları ve komutlar yeni paket yapısına göre yenilendi.

## [2026-08-18]

### Eklendi
- `.gitattributes`: `.bat` ve `.cmd` dosyalarının Git ve ZIP arşivlerinde `CRLF` satır sonunu koruması için kural eklendi.

### Düzeltildi
- `install.bat`, `run_dash.bat` ve `check_telemetry.bat`: Unix `LF` satır sonlarında `cmd.exe` çökmesini önlemek için çok satırlı `if (...)` blokları `goto` etiketli dallanmalara çevrildi.

## [2026-08-16 - 2026-08-17]

### Eklendi
- `setup_wizard.py`: Başlangıçta dil seçimi (`en`/`tr`) sunan iki dilli kurulum akışı eklendi.
- `check_telemetry.bat`: Windows'ta `telemetry_check.py` aracını sanal ortam içinden çalıştıran başlatıcı eklendi.

### Değiştirildi
- `install.bat` ve `run_dash.bat`: Terminal çıktıları `[1/3]`, `[2/3]`, `[3/3]` adımlarıyla İngilizce olarak düzenlendi.
- `telemetry_check.py`: Konsol durum ve hata mesajları İngilizceye çevrildi.
- Kurulum sonu özetinde `telemetry_check` adımı ve sanal ortam komutları öne çıkarıldı.

## [2026-08-15]

### Eklendi
- Windows'ta Python 3.12 sanal ortamı kuran `install.bat` ve göstergeyi açan `run_dash.bat` eklendi.
- `config.py` ve DiRT Rally 2.0 XML dosyasını yedekleyip güncelleyen `setup_wizard.py` eklendi.
- `AGENTS.md` geliştirici yönerge dosyası eklendi.

### Değiştirildi
- Proje dokümanları `docs/` dizinine taşındı.
- Windows ve Raspberry Pi bağımlılıkları ayrıldı; Python sürümü 3.12 ile sınırlandı.
- `README.md`, `CONFIGURATION.md` ve `ARCHITECTURE.md` yeni kurulum adımlarına göre güncellendi.

## [2026-08-13]

### Değiştirildi
- `git filter-repo` ile depo geçmişi temizlendi: eski `venv/` kayıtları silindi, yazar/committer bilgileri `alpivenator` olarak sabitlendi ve `origin` adresi güncellendi (depo boyutu ~14 MiB -> ~353 KiB).
- `ROADMAP.md`: Tamamlanan hassas veri taraması maddesi kaldırılıp notlar düzeltildi.

## [2026-08-05]

### Eklendi
- `LICENSE`: GPL-3.0 lisansı eklendi (telif: Alperen / alpivenator, 2026).
- `pyproject.toml`: Paket meta verileri eklendi (`name = "dirtdash"`, `version = "0.1.0a1"`, `license = "GPL-3.0-only"`, `requires-python = ">=3.12"`).

### Değiştirildi
- `settings.py`, `digital_dash.py` ve `analog_dash.py`: Pencere boyutları `settings.py` içindeki `DIGITAL_WIDTH/HEIGHT` ve `ANALOG_WIDTH/HEIGHT` değişkenlerine bağlandı.
- `CONFIG.md` dosyası `CONFIGURATION.md` adıyla yenilenip `config.py`, `settings.py`, `0.0.0.0` dinleme ve güvenlik notlarıyla genişletildi.
- `README.md`: Özellikler, gereksinimler, hızlı başlangıç, yapılandırma ve lisans bölümleriyle genişletildi.

## [2026-07-14 - 2026-07-31]

### Eklendi
- `ARCHITECTURE.md`, `CHANGELOG.md` ve `ROADMAP.md` dosyaları oluşturuldu.
- `pyproject.toml` dosyasına Black ve Ruff ayarları eklendi.

### Değiştirildi
- `udp_listener.py`: Soket zaman aşımı, tampon boşaltma döngüsü ve birim dönüşümleri satır içi yorumlarla açıklandı.
- `ROADMAP.md`: Eski alfa hedefleri beş ana başlık altında toplandı.

## [Erken geliştirme dönemi (2026-02 - 2026-06)]

İlk prototip ve alfa dönemi özetleri:

- Telemetri ve UDP dinleyicisi (`core/udp_listener.py`): DiRT Rally 2.0 Extradata=3 paketleri için 264 baytlık UDP soket dinleyicisi, `struct.unpack` ayrıştırıcısı ve eski paketleri atan tampon boşaltma döngüsü yazıldı.
- Dijital gösterge (`dashboards/digital_dash.py`): Koyu temalı dijital HUD, dinamik devir çubuğu, tekerlek kayması (SLIP) uyarısı ve gaz/fren çubukları eklendi.
- Analog gösterge (`dashboards/analog_dash.py`): Trigonometrik ibre çizimi, doğrusal yumuşatma, 9000 RPM kadran ve araca göre değişen redline bölgesi geliştirildi.
- Raspberry Pi vites ışıkları (`core/led_controller.py`): `gpiozero` üzerinden Yeşil -> Mavi -> Kırmızı GPIO vites ışığı kontrolü eklendi.
- Windows şeffaf overlay (`core/overlay_win.py`): Win32 `ctypes` çağrılarıyla çerçevesiz, tıklama geçirgen (`WS_EX_TRANSPARENT`), katmanlı (`alpha` / `chroma`) ve daima en üstte (`HWND_TOPMOST`) pencere desteği eklendi.
- Yapılandırma ve ölçekleme (`config.py`, `settings.py`): Sistem ve görsel ayarlar ayrıştırıldı; `TARGET_WIDTH` tabanlı orantılı ölçekleme ve `DASH_STYLE` seçimi merkezileştirildi.
