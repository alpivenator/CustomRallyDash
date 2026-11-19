# Changelog

[Türkçe](CHANGELOG_TR.md) | **English**

Notable changes to this project are listed in reverse chronological order. For planned work, see [ROADMAP.md](ROADMAP.md); for technical design, see [ARCHITECTURE.md](ARCHITECTURE.md).

## [v0.1.1] - 2026-09-09

### Changed
- `pyproject.toml`: Bumped package version to `0.1.1`.

### Fixed
- `install.bat`: Fixed Python version detection failing on systems without Python 3.13 due to signed `errorlevel` handling in Windows Batch, and added a fallback to the default `python` on `PATH`.

## [v0.1.0] - 2026-09-08

### Added
- `.github/workflows/ci.yml`: Added a `pip-audit` step to scan dependencies in CI.
- `pyproject.toml`: Enabled Ruff security rules (`"S"`) in `lint.select` and added `per-file-ignores` for test assertions and test XML parsing (`tests/* = ["S101", "S314"]`).

### Security
- `core/udp_listener.py` and `tools/mock_telemetry.py`: Updated socket bind suppressions to `# noqa: S104`.
- `tools/setup_wizard.py`: Annotated local game XML parsing with `# noqa: S314`.

### Note
- Evaluated Python 3.14 support and deferred it because Pygame 2.6.1 prebuilt wheels are not available on PyPI yet. Runtime requirement remains `>=3.11,<3.14`.

## [2026-09-03]

### Added
- `README_TR.md`: Added a Turkish version of the project overview and quick-start guide with language switcher links.
- `docs/CONFIGURATION_TR.md`: Added a Turkish configuration reference.
- `docs/ARCHITECTURE_TR.md`: Added a Turkish architecture and data-flow reference.

### Changed
- `docs/CONFIGURATION.md`: Moved common settings into a "Quick Configuration" table at the top and reorganized the remaining options by scope.
- `README.md` and `docs/ARCHITECTURE.md`: Added language switcher links at the top and tightened technical descriptions.
- `AGENTS.md`: Updated contributor guidelines to keep English and Turkish docs synchronized.
- Renamed the project to **CustomRallyDash** and updated `pyproject.toml` metadata (`name = "custom-rally-dash"`, `version = "0.1.0"`).
- Updated CLI banner headers in `tools/setup_wizard.py`.
- Changed project license from GPL-3.0 to MIT in `LICENSE`, `README.md`, and `pyproject.toml`.

## [2026-09-02]

### Added
- `README.md`: Added an in-game transparent digital hood HUD screenshot as the main preview image.
- `images/`: Converted screenshot assets to WebP, reducing asset size by over 90%.

### Changed
- `pyproject.toml`, `README.md`, `install.bat`, `.github/workflows/ci.yml`, `docs/ARCHITECTURE.md`: Updated Python support to `>=3.11,<3.14` (3.11, 3.12, and 3.13), set CI default to Python 3.13, and updated `install.bat` to detect Python 3.13, 3.12, or 3.11.

## [2026-09-01]

### Added
- `dashboards/digital_dash.py` and `dashboards/analog_dash.py`: Added dark text outlines (`draw_text_outlined`, `draw_text_outlined_center`) on gauge readouts and labels to improve legibility over bright stages in transparent overlay mode.
- `settings.py`: Added `COLOR_TEXT_OUTLINE` (default `(0, 0, 0)`) to configure text outline color.
- `README.md`: Noted that DiRT Rally 2.0 must run in Windowed or Borderless Windowed mode for the Windows overlay to remain visible.
- `tests/test_themes_and_mock.py`: Added unit tests for overlay settings and outlined text rendering.

### Changed
- `config.py` and `settings.py`: Kept only `ENABLE_OVERLAY` in `config.py` and moved visual and placement settings (`OVERLAY_MODE`, `OVERLAY_POSITION`, `OVERLAY_MARGIN`, `OVERLAY_ALPHA`, `OVERLAY_CHROMA_KEY`) to `settings.py`.
- `settings.py`: Set default `OVERLAY_MODE` to `"chroma"` and `OVERLAY_POSITION` to `"bottom-right"`, and aliased `OVERLAY_CHROMA_KEY = COLOR_BG` so it tracks the active theme.
- `settings.py` and `dashboards/themes.py`: Changed default `COLOR_REDLINE` to `(255, 65, 105, 110)` so the redline sector stays distinct from the warning needle color.
- `core/overlay_win.py`: Updated default parameters for `apply_overlay` (`mode="chroma"`) and `position_window` (`position="bottom-right"`).
- `dashboards/analog_dash.py` and `dashboards/digital_dash.py`: Simplified RPM warning lookup to read `settings.RPM_WARNING_THRESHOLD` directly.
- `tools/setup_wizard.py`: Added offline preview (`run_mock.bat` / `--mock`) and theme selector (`select_theme.bat`) steps to the setup completion summary (EN and TR).
- `README.md`: Rewrote the README with compact quick-start tables and CLI commands.
- `config.py`: Set default `DASH_STYLE` to `"digital"`.
- `docs/CONFIGURATION.md`: Documented `select_theme.bat` and `run_mock.bat`, added dashboard style options, and moved overlay settings into the visual settings table.
- `docs/ARCHITECTURE.md`: Updated Windows overlay notes to match `settings.py` ownership.

### Fixed
- `dashboards/analog_dash.py`: Replaced `pygame.draw.arc` with a trigonometric polygon fill (`pygame.draw.polygon`) in `draw_redline_zone` to fix rasterization gaps, moiré patterns, and dark pixel artifacts.

## [2026-08-31]

### Added
- `settings.py`: Added `RPM_WARNING_THRESHOLD` (default `0.90`) to control when tachometers switch to the warning color.
- `tests/test_themes_and_mock.py`: Added a unit test verifying `settings.RPM_WARNING_THRESHOLD`.

### Changed
- `dashboards/analog_dash.py`: Switched the needle warning color trigger from 100% redline to `max_rpm * RPM_WARNING_THRESHOLD`.
- `dashboards/analog_dash.py`: Increased stroke width of the central gear housing accent ring.
- `dashboards/digital_dash.py`: Switched the RPM bar warning color trigger to `settings.RPM_WARNING_THRESHOLD`.
- `README.md` and `docs/CONFIGURATION.md`: Added Windows instructions for unblocking downloaded ZIP archives before extracting them.

### Fixed
- `pyproject.toml`: Added `[tool.pytest.ini_options]` with `pythonpath = ["."]` and `testpaths = ["tests"]` so imports (`tools`, `dashboards`, `core`) resolve in both local and CI runs.
- `.github/workflows/ci.yml`: Standardized test execution to `python -m pytest`.

## [2026-08-29]

### Changed
- `tools/mock_telemetry.py`: Tuned the mock telemetry loop to a 15-second WRC acceleration cycle, shifting gears 1 to 6 over 9 seconds (~1.5s per gear) up to 205 km/h.
- `tools/mock_telemetry.py`: Modeled close-ratio sequential gearing starting at 2500 RPM in 1st gear with upshifts dropping to ~5800 RPM.
- `tools/mock_telemetry.py`: Added progressive downshifting (6 to 1) with simulated ~50% throttle auto-blip pulses and ~6800 RPM rev-matching spikes across the 9-15s braking phase.

### Fixed
- `tools/mock_telemetry.py`: Extended deceleration down to 1st gear and idle/stop so the 15-second loop restarts without abrupt gear or RPM jumps.

## [2026-08-28]

### Added
- `dashboards/themes.py`: Added five color themes (`modern_dark`, `subaru_classic`, `gt3_racing`, `night_neon`, `retro_amber`).
- `tools/theme_selector.py` and `select_theme.bat`: Added a bilingual (EN/TR) CLI theme switcher and Windows launcher that backs up and updates `settings.py`.
- `tools/mock_telemetry.py` and `run_mock.bat`: Added a 60 Hz Extradata=3 synthetic UDP generator simulating acceleration, sequential shifts, braking, and corner exits.
- `main.py`: Added `--mock` flag to run the dashboard and mock telemetry generator together (`python main.py --mock`).
- `.github/ISSUE_TEMPLATE/`: Added `bug_report.yml` and `feature_request.yml` issue templates.
- `tests/test_themes_and_mock.py`: Added unit tests for mock packet generation and theme switching.

### Changed
- `dashboards/analog_dash.py`: Updated drawing order for the needle, center pivot, and gear dial.
- `README.md`, `ARCHITECTURE.md`, and `ROADMAP.md`: Updated docs for the theme system, mock preview tools, and package structure.

## [2026-08-20]

### Refactored
- `core/`: Moved UDP listener, Windows overlay, and GPIO LED driver into `core/` (`udp_listener.py`, `overlay_win.py`, `led_controller.py`) with exports in `core/__init__.py`.
- `dashboards/`: Moved digital and analog dashboards into `dashboards/` (`digital_dash.py`, `analog_dash.py`) and renamed `analogdash.py` to `analog_dash.py`.
- `tools/`: Moved setup and diagnostic scripts into `tools/` (`setup_wizard.py`, `telemetry_check.py`) with dynamic project root path resolution.
- `main.py`: Updated imports to `dashboards.digital_dash` and `dashboards.analog_dash`.
- `install.bat` and `check_telemetry.bat`: Updated paths to `tools\setup_wizard.py` and `tools\telemetry_check.py`.
- `tests/test_setup_wizard.py`: Updated tests for `tools.setup_wizard` and `tools.telemetry_check`.
- `ARCHITECTURE.md`, `CONFIGURATION.md`, and `README.md`: Updated file paths and commands for the package layout.

## [2026-08-18]

### Added
- `.gitattributes`: Enforced CRLF line endings for `.bat` and `.cmd` files in Git and ZIP archives.

### Fixed
- `install.bat`, `run_dash.bat`, and `check_telemetry.bat`: Replaced multiline `if (...)` blocks with `goto` label branching to avoid `cmd.exe` crashes under Unix LF line endings.

## [2026-08-16 - 2026-08-17]

### Added
- `setup_wizard.py`: Added bilingual (EN/TR) first-run setup flow.
- `check_telemetry.bat`: Added a Windows launcher for `telemetry_check.py`.

### Changed
- `install.bat` and `run_dash.bat`: Standardized English terminal output into `[1/3]`, `[2/3]`, and `[3/3]` steps.
- `telemetry_check.py`: Standardized console messages to English.
- Highlighted `telemetry_check` and virtual environment commands in the setup summary.

## [2026-08-15]

### Added
- Added `install.bat` (Python 3.12 virtual environment setup on Windows) and `run_dash.bat`.
- Added `setup_wizard.py` to back up and patch `config.py` and DiRT Rally 2.0's telemetry XML.
- Added `AGENTS.md` local contributor guide.

### Changed
- Moved project documentation into `docs/`.
- Split Windows and Raspberry Pi dependencies and restricted runtime to Python 3.12.
- Updated `README.md`, `CONFIGURATION.md`, and `ARCHITECTURE.md` for the new setup scripts.

## [2026-08-13]

### Changed
- Cleaned repository history with `git filter-repo`: purged old `venv/` commits, standardized author/committer metadata to `alpivenator`, and updated `origin` (reducing repo size from ~14 MiB to ~353 KiB).
- `ROADMAP.md`: Removed the completed sensitive-data scan item and updated notes.

## [2026-08-05]

### Added
- `LICENSE`: Added GPL-3.0 license (Copyright Alperen / alpivenator, 2026).
- `pyproject.toml`: Added package metadata (`name = "dirtdash"`, `version = "0.1.0a1"`, `license = "GPL-3.0-only"`, `requires-python = ">=3.12"`).

### Changed
- `settings.py`, `digital_dash.py`, and `analog_dash.py`: Bound window dimensions to `DIGITAL_WIDTH/HEIGHT` and `ANALOG_WIDTH/HEIGHT` in `settings.py`.
- Renamed `CONFIG.md` to `CONFIGURATION.md` and expanded it with `config.py`, `settings.py`, `0.0.0.0` binding, and security notes.
- Expanded `README.md` with features, requirements, quick start, configuration, and license sections.

## [2026-07-14 - 2026-07-31]

### Added
- Added `ARCHITECTURE.md`, `CHANGELOG.md`, and `ROADMAP.md`.
- Added `pyproject.toml` with Black and Ruff lint/format configuration.

### Changed
- `udp_listener.py`: Documented socket timeout, packet drain loop, and telemetry unit conversions inline.
- `ROADMAP.md`: Grouped early alpha items into five milestone sections.

## [Early Development Phase (2026-02 - 2026-06)]

Initial prototype and alpha milestones:

- Telemetry and UDP listener (`core/udp_listener.py`): Built a 264-byte UDP socket listener and `struct.unpack` parser for DiRT Rally 2.0 Extradata=3 packets with a drain loop to drop stale frames.
- Digital dashboard (`dashboards/digital_dash.py`): Implemented dark-themed digital HUD with RPM bar, tire-slip warning, throttle/brake bars, and gear/speed readouts.
- Analog dashboard (`dashboards/analog_dash.py`): Implemented a 9000 RPM analog dial with trigonometric needle rendering, linear smoothing, and dynamic redline zone.
- Raspberry Pi shift lights (`core/led_controller.py`): Added Green -> Blue -> Red GPIO shift lights via `gpiozero`.
- Windows transparent overlay (`core/overlay_win.py`): Integrated Win32 `ctypes` calls for borderless, click-through (`WS_EX_TRANSPARENT`), layered (`alpha` / `chroma`), always-on-top (`HWND_TOPMOST`) windows.
- Configuration and scaling (`config.py`, `settings.py`): Separated system settings from visual layout options with proportional scaling (`TARGET_WIDTH`) and `DASH_STYLE` switching.
