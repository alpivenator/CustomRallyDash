# Changelog

All notable changes to this project are documented in this file in reverse chronological order.
For planned milestones, see `ROADMAP.md`. For technical architecture, see `ARCHITECTURE.md`.

## [2026-08-29]

### Changed
- `tools/mock_telemetry.py`: Tuned telemetry simulation loop to a 15-second cycle matching modern WRC acceleration dynamics; shifts through gears 1 to 6 in 9 seconds (~1.5s per gear) reaching a top speed of 205 km/h.
- `tools/mock_telemetry.py`: Modeled close-ratio sequential transmission dynamics; launch starts at 2500 RPM in 1st gear, with subsequent upshifts dropping engine speed to ~5800 RPM.
- `tools/mock_telemetry.py`: Added progressive downshifting (6->1), simulated ECU auto-blip throttle pulses (~50%), and rev-matching dynamics (~6800 RPM spikes with engine braking decay) across the 9-15s braking phase.

### Fixed
- `tools/mock_telemetry.py`: Extended deceleration phase down to 1st gear and idle/stop, eliminating abrupt gear/RPM jumps when the 15-second loop restarts.

---

## [2026-08-28]

### Added
- `dashboards/themes.py`: Added 5 curated motorsport-inspired color themes (`modern_dark`, `subaru_classic`, `gt3_racing`, `night_neon`, `retro_amber`).
- `tools/theme_selector.py` & `select_theme.bat`: Added bilingual (EN/TR) interactive CLI tool and Windows launcher to switch presets safely without breaking `settings.py`.
- `tools/mock_telemetry.py` & `run_mock.bat`: Added lightweight synthetic 60 Hz Extradata=3 UDP generator simulating acceleration, sequential gear shifts, hard braking, and corner exits.
- `main.py`: Added `--mock` flag to run dashboard and synthetic telemetry generator concurrently (`python main.py --mock`).
- `.github/ISSUE_TEMPLATE/`: Added `bug_report.yml` and `feature_request.yml` issue forms for GitHub.
- `tests/test_themes_and_mock.py`: Added unit tests verifying synthetic packet generation and theme application logic.

### Changed
- `dashboards/analog_dash.py`: Modernized analog gauge rendering hierarchy including needle, center pivot, and gear indicator housing.
- `README.md`, `ARCHITECTURE.md`, `ROADMAP.md`: Updated documentation to reflect theme architecture, mock preview utilities, and modular structure.

---

## [2026-08-20]

### Refactored
- `core/`: Moved telemetry decoder, overlay, and hardware drivers into `core/` package (`core/udp_listener.py`, `core/overlay_win.py`, `core/led_controller.py`) with clean package exports in `core/__init__.py`.
- `dashboards/`: Moved digital and analog dashboard implementations into `dashboards/` package (`dashboards/digital_dash.py`, `dashboards/analog_dash.py`); normalized `analogdash.py` to `analog_dash.py`.
- `tools/`: Moved setup wizard and diagnostic utilities into `tools/` package (`tools/setup_wizard.py`, `tools/telemetry_check.py`); enabled dynamic root path resolution in `setup_wizard.py` and `telemetry_check.py`.
- `main.py`: Updated imports to new package paths `dashboards.digital_dash` and `dashboards.analog_dash`.
- `install.bat` & `check_telemetry.bat`: Updated batch targets to `tools\setup_wizard.py` and `tools\telemetry_check.py`.
- `tests/test_setup_wizard.py`: Updated unit tests for `tools.setup_wizard` and `tools.telemetry_check`.
- Documentation (`ARCHITECTURE.md`, `CONFIGURATION.md`, `README.md`): Updated all references to reflect the modular package structure.

---

## [2026-08-18]

### Added
- `.gitattributes`: Added repository attribute ensuring `.bat` and `.cmd` files retain CRLF line endings across Git and ZIP archives.

### Fixed
- `install.bat`, `run_dash.bat`, `check_telemetry.bat`: Replaced multiline `if (...)` parenthesis blocks with `goto` and label-based branching to prevent `cmd.exe` crashes under Unix LF line endings.

---

## [2026-08-16 – 2026-08-17]

### Added
- `setup_wizard.py`: Added bilingual setup wizard supporting English and Turkish CLI flows.
- `check_telemetry.bat`: Added one-click diagnostic launcher for Windows.

### Changed
- `install.bat` & `run_dash.bat`: Standardized terminal output into structured `[1/3]`, `[2/3]`, `[3/3]` installation steps in English.
- `telemetry_check.py`: Standardized console status and diagnostic messages to English.

---

## [2026-08-15]

### Added
- Added `install.bat` for automated Python 3.12 virtual environment setup on Windows and `run_dash.bat` launcher.
- Added `setup_wizard.py` to configure `config.py` and patch DiRT Rally 2.0 telemetry XML with automatic timestamped backups.
- Added `AGENTS.md` local development guideline.

### Changed
- Moved project documentation under `docs/` directory.
- Separated Windows and Raspberry Pi dependencies; restricted supported runtime to Python 3.12.
- Updated `README.md`, `CONFIGURATION.md`, and `ARCHITECTURE.md` to reflect new setup flows.

---

## [2026-08-13]

### Changed
- Repository history cleanup via `git filter-repo`: Purged historical `venv/` commits, standardized commit author/committer identity to `alpivenator`, updated remote origin (repo size reduced ~14 MiB → ~353 KiB).
- `ROADMAP.md`: Removed completed sensitive data scan task; refined notes.

---

## [2026-08-05]

### Added
- `LICENSE`: Added GPL-3.0 license (Copyright Alperen / alpivenator, 2026).
- `pyproject.toml`: Added project metadata (`name = "dirtdash"`, `version = "0.1.0a1"`, `license = "GPL-3.0-only"`, `requires-python = ">=3.12"`).

### Changed
- `settings.py` / `digital_dash.py` / `analog_dash.py`: Bound window dimensions dynamically to `settings.py` parameters (`DIGITAL_WIDTH/HEIGHT`, `ANALOG_WIDTH/HEIGHT`).
- `CONFIG.md` → `CONFIGURATION.md`: Renamed and expanded with comprehensive configuration references, `0.0.0.0` binding notes, and security considerations.
- `README.md`: Expanded with feature matrix, system requirements, quick-start guide, and configuration summaries.

---

## [2026-07-14 – 2026-07-31]

### Added
- Added `ARCHITECTURE.md`, `CHANGELOG.md`, and `ROADMAP.md`.
- Added `pyproject.toml` with `black` and `ruff` linting/formatting configuration.

### Changed
- `udp_listener.py`: Added inline documentation for socket timeout handling, buffer drain loop, and telemetry conversion maths.
- `ROADMAP.md`: Consolidated early alpha phases into five structured milestone categories.

---

## [Early Development Phase (2026-02 – 2026-06)]

Summary of initial prototype and alpha development milestones:

- **Telemetry & UDP Listener (`core/udp_listener.py`):** Built raw 264-byte UDP socket listener and `struct.unpack` parser for DiRT Rally 2.0 Extradata=3 format with packet drain mechanism to eliminate latency.
- **Digital Dashboard (`dashboards/digital_dash.py`):** Implemented compact dark-themed digital UI with dynamic RPM bar, tire slip traction warning, throttle/brake pedal bars, and WRC/F1-inspired layout.
- **Analog Dashboard (`dashboards/analog_dash.py`):** Implemented analog gauge with trigonometric needle rendering, linear interpolation smoothing, 9000 RPM dial, and dynamic redline scaling.
- **Raspberry Pi Shift Lights (`core/led_controller.py`):** Implemented Green → Blue → Red shift-light sequence on GPIO pins via `gpiozero`.
- **Windows Transparent Overlay (`core/overlay_win.py`):** Implemented Win32 API (`ctypes`) integration for borderless, click-through (`WS_EX_TRANSPARENT`), layered (`alpha` / `chroma`), always-on-top (`HWND_TOPMOST`) overlay mode.
- **Configuration & Theming (`config.py` & `settings.py`):** Decoupled system hardware settings from visual styling parameters with automatic proportional scaling.

