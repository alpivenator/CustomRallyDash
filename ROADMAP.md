# Yol Haritası (Roadmap)

Bu dosya **yalnızca tamamlanmamış hedefleri** içerir. Tamamlanan çalışmalar
`CHANGELOG.md` içinde, mimari bilgi ise `ARCHITECTURE.md` içindedir. Dosya şimdilik Türkçedir.

> **Not:** Bu dosyanın "Hedefler" bölümü yönetici tarafından güncellenir.
> Yapay zeka veya herhangi bir kullanıcı, istenmedikçe, buraya yeni hedef eklemez.

## Yayın & Güvenlik

- [ ] **Hassas veri taraması:** Geçmişteki e-postalar + venv geçmişi. İki seçenek: (a) GitHub Settings'te "Block command line pushes that expose my email" ayarını aç; (b) geçmişi `git filter-repo` ile yeniden yaz (repo daha public değilken yapılırsa sorunsuz). Önerilen: (a).
- [ ] **GitHub Releases:** v0.1.0-alpha yayınla (tag + kaynak zip yeterli).
- [ ] **GitHub'da public yap** — son adım.
- [ ] **CI (isteğe bağlı):** Public'e açtıktan sonra GitHub Actions ile ruff + bandit.
- [ ] **Güvenlik:** Programın güvenlik testleri (planlanacak).


## Arayüz & Özelleştirme

- [ ] **Görsel İyileştirme (analogdash):** Estetik pivot noktası, geliştirilmiş renk paleti ve merkezi vites dairesi.
- [ ] **Tema Sistemi:** Hazır tema paketleri (Dark, WRC Classic, Neon, Minimalist). Kullanıcılar kendi temalarını oluşturup paylaşabilir.
- [ ] **Örnek Tema Dosyaları:** Kullanıcıların başlaması için hazır şablonlar.
- [ ] **Linux Overlay Desteği:** X11/Wayland üzerinde saydam overlay penceresi (ileri dönem). **[Öncelik: düşük]**

## Kullanım Kolaylığı

- [ ] **Windows Başlangıç Betiği:** Tek tıkla çalıştırma için `run_dash.bat` başlatıcı. Kolaylık için gerekli. **[Öncelik: yüksek]**
- [ ] **Kurulum Sihirbazı:** İlk çalıştırmada ayar dosyası oluşturma.

## Veri & Performans

- [ ] **Günlükleme Sistemi:** Analiz için telemetri verilerinin CSV/JSON formatında kaydedilmesi. **[Öncelik: düşük]**
- [ ] **Performans & Optimizasyon:** Programın daha verimli çalışması için yapılacak düzenlemeler.


