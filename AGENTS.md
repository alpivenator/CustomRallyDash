# Proje Talimatları

## Dil ve üslup

- Kaynak kod ve kod içi yorumlar İngilizce yazılır.
- Yorumları kısa ve açık tut. Önemsiz değişiklikler için yorum ekleme.
- `AGENTS.md` Türkçe tutulur ve depoda git ile izlenen proje kılavuzudur.
- Ana belgeler (`docs/CHANGELOG.md`, `docs/ROADMAP.md`, `docs/ARCHITECTURE.md`, `docs/CONFIGURATION.md`, `README.md`) İngilizce hazırlanır. Türkçe karşılıkları (`docs/CHANGELOG_TR.md`, `docs/ROADMAP_TR.md`, `docs/ARCHITECTURE_TR.md`, `docs/CONFIGURATION_TR.md`, `README_TR.md`) bunlarla eşzamanlı güncellenir.
- Kullanıcı talimatlarına uy. Planlanan ve uygulanan değişiklikleri açık biçimde özetle.

## Mimari

- Ayrıntılı yapı ve veri akışı için önce `docs/ARCHITECTURE.md` dosyasını incele.
- Uygulama, DiRT Rally 2.0'dan gelen 60 Hz UDP telemetrisini alıp dijital veya analog pygame gösterge panelinde gösterir.
- Uygulama `main.py` üzerinden başlar. Çalışma ayarları `config.py`, görsel ayarlar ise `settings.py` dosyasında tutulur.
- Windows overlay'i ve Raspberry Pi GPIO vites ışıkları isteğe bağlıdır.

## Doğrulama ve kalite kontrolleri

Python dosyalarını değiştirdikten sonra şu kontrolleri çalıştır:

- Testler: `pytest` (sanal ortamda `.venv/bin/python -m pytest -v`)
- Lint: `ruff check .`
- Biçimlendirme: `black --check .`
- Bağımlılık güvenliği (bağımlılık dosyaları değişirse): `pip-audit -r requirements.txt`

## Proje notları

### CHANGELOG güncelleme kuralları
- `docs/CHANGELOG.md` (EN) ve `docs/CHANGELOG_TR.md` (TR) yalnızca yeni sürüm çıkarken, en yeni en üstte olacak şekilde eşzamanlı güncellenir. GitHub Releases notları da buradaki girişleri temel alır.
- Ara geliştirme adımları için tarihli kayıt (`## [YYYY-MM-DD]`) açılmaz.
- Yeni sürüm başlıkları `## [vX.Y.Z] - YYYY-MM-DD` biçiminde eklenir ve Keep a Changelog kategorileri kullanılır:
  - EN: `### Added`, `### Changed`, `### Fixed`, `### Refactored`, `### Removed`, `### Security`
  - TR: `### Eklendi`, `### Değiştirildi`, `### Düzeltildi`, `### Refaktör`, `### Kaldırıldı`, `### Güvenlik`
- Her madde etkilenen modül ya da dosya adıyla birlikte yapılan değişikliği özetler.
- Eski kayıtlar ve erken dönem özetleri kronolojik sırası bozulmadan korunur.

### ROADMAP güncelleme kuralları
- `docs/ROADMAP.md` (EN) ve `docs/ROADMAP_TR.md` (TR) yalnızca açık ve planlanan hedefleri içerir.
- Bu dosyalardaki hedefleri yalnızca proje yöneticisinin (Alperen) açık isteğiyle güncelle. Talep edilmedikçe yeni hedef ekleme.


