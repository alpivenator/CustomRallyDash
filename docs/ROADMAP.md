# Roadmap

This document outlines **planned milestones and future goals** along with some recently competed goals for the project.
For completed work and version history, see `CHANGELOG.md`. For technical design, see `ARCHITECTURE.md`.

## Release & Security

- [x] **GitHub Releases:** Publish v0.1.0-alpha (git tag + source archive).
- [x] **Security Testing:** Baseline security testing and validation.
- [x] **Public Launch:** Make repository publicly available on GitHub.
- [x] **CI Pipeline:** Automated linting and test workflow via GitHub Actions (`ruff` + `pytest`).

## Usability & Setup

- [x] **Windows Launch Scripts:** One-click launch with `run_dash.bat` and automated virtual environment setup via `install.bat`.
- [x] **First-Run Setup Wizard:** Interactive CLI wizard to safely configure `config.py` and patch DiRT Rally 2.0 telemetry XML with automatic backups.

## Interface & Customization

- [x] **Visual Polish (Analog Dash):** Center pivot styling, refined color palette, and dedicated gear indicator dial.
- [x] **Theme System:** Curated motorsport theme presets in `dashboards/themes.py` (Subaru Classic, GT3 Racing, Night Neon, Retro Amber, Modern Dark).
- [x] **Theme Selector CLI:** Standalone interactive tool and Windows launcher (`tools/theme_selector.py`, `select_theme.bat`) to switch themes safely.
- [x] **Mock Telemetry & Live Preview:** Standalone 60 Hz UDP synthetic telemetry generator (`tools/mock_telemetry.py`, `main.py --mock`, `run_mock.bat`).
- [ ] **Linux Overlay Support:** Transparent click-through overlay on X11/Wayland. **[Priority: Low]**

## Data & Performance

- [ ] **Telemetry Logging:** Session recording to CSV/JSON for post-stage telemetry analysis. **[Priority: Low]**
- [ ] **Performance Profiling:** Frame-time and memory optimization for low-spec embedded hardware.

