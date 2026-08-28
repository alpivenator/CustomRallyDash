# Yol Haritası (Roadmap)

Bu dosya **yalnızca tamamlanmamış hedefleri** içerir. Tamamlanan çalışmalar
`CHANGELOG.md` içinde, mimari bilgi ise `ARCHITECTURE.md` içindedir. Dosya şimdilik Türkçedir.

> **Not:** Bu dosyadaki "hedefler" yöneticinin isteğiyle güncellenir.
> Yapay zeka veya herhangi bir kullanıcı, istenmedikçe, buraya yeni hedef eklemez.

## Yayın & Güvenlik

- [ ] **GitHub Releases:** v0.1.0-alpha yayınla (tag + kaynak zip yeterli).
- [ ] **Güvenlik:** Programın güvenlik testleri (planlanacak).
- [ ] **GitHub'da public yap** — son adım.
- [ ] **CI (isteğe bağlı):** Public'e açtıktan sonra GitHub Actions ile ruff + bandit.


## Kullanım Kolaylığı

- [x] **Windows Başlangıç Betiği:** `run_dash.bat` ile tek tıkla çalıştırma ve `install.bat` ile sanal ortam kurulumu tamamlandı.
- [x] **Kurulum Sihirbazı:** İlk çalıştırmada `config.py` ve oyun telemetry XML’i yedeklenerek yapılandırılıyor.

## Arayüz & Özelleştirme

- [x] **Görsel İyileştirme (analogdash):** Estetik pivot noktası, geliştirilmiş renk paleti ve merkezi vites dairesi.
- [x] **Tema Sistemi:** Hazır tema paketleri (`dashboards/themes.py` altında Subaru Classic, GT3, Neon, Retro Amber, Modern Dark).
- [x] **Tema ve Özelleştirme CLI Aracı:** Hazır temaları seçme ve kullanıcı görsel ayarlarını kolayca düzenleme (`tools/theme_selector.py`, `select_theme.bat`).
- [x] **Mock / Canlı Önizleme Sistemi:** Oyunu açmadan 60 Hz UDP simülasyonu ile canlı önizleme (`tools/mock_telemetry.py`, `main.py --mock`, `run_mock.bat`).
- [ ] **Linux Overlay Desteği:** X11/Wayland üzerinde saydam overlay penceresi (ileri dönem). **[Öncelik: düşük]**


## Veri & Performans

- [ ] **Günlükleme Sistemi:** Analiz için telemetri verilerinin CSV/JSON formatında kaydedilmesi. **[Öncelik: düşük]**
- [ ] **Performans & Optimizasyon:** Programın daha verimli çalışması için yapılacak düzenlemeler.
