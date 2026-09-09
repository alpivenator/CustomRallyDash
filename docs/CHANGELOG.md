# Changelog

All notable changes to this project are documented in this file in reverse chronological order.
For planned milestones, see `ROADMAP.md`. For technical architecture, see `ARCHITECTURE.md`.

## [v0.1.0] - 2026-09-08

### Added
- `.github/workflows/ci.yml`: Added `pip-audit` step to automate dependency vulnerability scanning in CI/CD pipeline.
- `pyproject.toml`: Added Ruff security rules (`"S"`) to `lint.select` and configured `per-file-ignores` for test assert statements and XML parses (`tests/* = ["S101", "S314"]`).

### Security
- `core/udp_listener.py` & `tools/mock_telemetry.py`: Updated socket binding suppressions to Ruff `# noqa: S104` format.
- `tools/setup_wizard.py`: Annotated local game configuration XML parsing with `# noqa: S314`.

### Note
- Evaluated Python 3.14 compatibility; support is currently deferred due to Pygame 2.6.1 prebuilt wheel availability constraints on PyPI. Python runtime requirement remains locked to `>=3.11,<3.14`.

## 2026-09-03

### Added
- `README_TR.md`: Added comprehensive Turkish translation of project overview and quick-start guide with cross-language navigation.
- `docs/CONFIGURATION_TR.md`: Added full Turkish translation of configuration reference with clear technical terminology.
- `docs/ARCHITECTURE_TR.md`: Added full Turkish translation of technical architecture and runtime/data flow specifications.

### Changed
- `docs/CONFIGURATION.md`: Restructured and streamlined configuration reference with a high-priority "Quick Configuration" table upfront, logical categorization of settings, and objective technical phrasing.
- `README.md` & `docs/ARCHITECTURE.md`: Added header language switcher links and replaced promotional wording with precise technical descriptions.
- `AGENTS.md`: Updated developer guidelines to maintain full synchronization across all English and Turkish documentation counterparts.
- Renamed project to **CustomRallyDash** and updated `pyproject.toml` package metadata (`name = "custom-rally-dash"`, `version = "0.1.0"`).
- Updated CLI setup wizard banner headers in `tools/setup_wizard.py`.
- Updated project license from GPL-3.0 to MIT in `LICENSE`, `README.md`, and `pyproject.toml`.

## [2026-09-02]

### Added
- `README.md`: Added in-game transparent digital hood HUD screenshot as the primary hero preview banner.
- `images/`: Converted and optimized screenshot assets to high-compression WebP format, reducing asset footprint by over 90%.

### Changed
- `pyproject.toml`, `README.md`, `install.bat`, `.github/workflows/ci.yml`, `docs/ARCHITECTURE.md`: Updated Python runtime requirements to support Python 3.11, 3.12, and 3.13 (`>=3.11,<3.14`), set default CI target to Python 3.13, and updated `install.bat` to detect and use Python 3.13, 3.12, or 3.11.

## [2026-09-01]

### Added
- `dashboards/digital_dash.py` & `dashboards/analog_dash.py`: Added high-contrast dark text outline strokes (`draw_text_outlined`, `draw_text_outlined_center`) across all gauge readouts, labels, and markings for crystal-clear readability over bright in-game stages in transparent overlay HUD mode.
- `settings.py`: Added `COLOR_TEXT_OUTLINE` setting (default `(0, 0, 0)`) for customising text outline contrast.
- `README.md`: Added note specifying DiRT Rally 2.0 must run in Windowed or Borderless Windowed mode for the Windows click-through overlay to remain visible.
- `tests/test_themes_and_mock.py`: Added unit tests verifying overlay settings structure and text outline rendering.

### Changed
- `config.py` & `settings.py`: Refactored overlay configuration architecture by keeping only `ENABLE_OVERLAY` toggle in `config.py` and migrating all visual/window positioning settings (`OVERLAY_MODE`, `OVERLAY_POSITION`, `OVERLAY_MARGIN`, `OVERLAY_ALPHA`, `OVERLAY_CHROMA_KEY`) into `settings.py`.
- `settings.py`: Set default `OVERLAY_MODE` to `"chroma"` and `OVERLAY_POSITION` to `"bottom-right"`, dynamically aliasing `OVERLAY_CHROMA_KEY = COLOR_BG` for automatic synchronization with active color themes.
- `settings.py` & `dashboards/themes.py`: Updated `COLOR_REDLINE` default to a brighter, soft rose-red tone (`(255, 65, 105, 110)`) distinct from the warning needle color.
- `core/overlay_win.py`: Updated default argument values for `apply_overlay` (`mode="chroma"`) and `position_window` (`position="bottom-right"`).
- `dashboards/analog_dash.py` & `dashboards/digital_dash.py`: Simplified RPM warning threshold lookup to direct `settings.RPM_WARNING_THRESHOLD` attribute access.
- `tools/setup_wizard.py`: Expanded setup completion next-steps instructions (EN & TR) to include offline preview (`run_mock.bat` / `--mock`) and theme selector (`select_theme.bat`).
- `README.md`: Refactored documentation with a clean, engineering-focused structure featuring concise Quick Start tables, clear CLI workflows, and zero boilerplate.
- `config.py`: Set default `DASH_STYLE` to `"digital"` as the recommended compact horizontal bar HUD layout.
- `docs/CONFIGURATION.md`: Added dedicated quick-start guidance and documentation for `select_theme.bat` and `run_mock.bat`, added dashboard style section detailing digital HUD as default, and moved overlay settings to the visual settings table.
- `docs/ARCHITECTURE.md`: Updated Windows overlay architecture documentation to reflect `settings.py` parameter ownership.

### Fixed
- `dashboards/analog_dash.py`: Replaced `pygame.draw.arc` with a smooth trigonometric pie-sector polygon fill (`pygame.draw.polygon`) in `draw_redline_zone`, eliminating rasterization gaps, moiré patterns, and black pixel artifacts.


---

## [2026-08-31]

### Added
- `settings.py`: Added `RPM_WARNING_THRESHOLD` configuration setting (default `0.90`) to centrally configure the threshold at which tachometers shift to warning colour.
- `tests/test_themes_and_mock.py`: Added unit test verifying the `settings.RPM_WARNING_THRESHOLD` configuration value.

### Changed
- `dashboards/analog_dash.py`: Updated needle warning colour trigger to switch to `RPM_WARNING` when engine RPM reaches `max_rpm * RPM_WARNING_THRESHOLD` rather than only at 100% redline.
- `dashboards/analog_dash.py`: Increased stroke width of the central gear housing accent ring for enhanced contrast and visual prominence.
- `dashboards/digital_dash.py`: Standardised the RPM bar warning color transition against `settings.RPM_WARNING_THRESHOLD`.
- `README.md` & `docs/CONFIGURATION.md`: Added Windows installation instructions on unblocking downloaded ZIP archives before extracting and running batch scripts.

### Fixed
- `pyproject.toml`: Added `[tool.pytest.ini_options]` configuration defining `pythonpath = ["."]` and `testpaths = ["tests"]` to resolve module imports (`tools`, `dashboards`, `core`) seamlessly across local and CI test environments.
- `.github/workflows/ci.yml`: Standardized test execution to `python -m pytest` ensuring consistent runner execution.

---

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

